"""
LLM Orchestrator
Handles query classification, routing, and response generation
"""
from typing import Dict, List, Optional
import google.generativeai as genai
import config
from src.employee_lookup import get_employee_lookup
from src.rag_pipeline import get_rag_pipeline


class LLMOrchestrator:
    """
    Orchestrates LLM interactions, query routing, and response generation
    """
    
    def __init__(self):
        """
        Initialize LLM orchestrator
        """
        self.employee_lookup = get_employee_lookup()
        self.rag_pipeline = get_rag_pipeline()
        self._initialize_llm()
    
    def _initialize_llm(self):
        """
        Initialize Google Gemini LLM
        """
        try:
            if not config.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not found")
            
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(config.MODEL_NAME)
            print("✓ LLM initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing LLM: {e}")
            raise
    
    def classify_query(self, query: str) -> Dict[str, bool]:
        """
        Classify query to determine which tools to use
        
        Args:
            query: User query
            
        Returns:
            Dictionary with classification results
        """
        query_lower = query.lower()
        
        # Check for employee-specific keywords
        needs_employee_data = any(
            keyword in query_lower 
            for keyword in config.EMPLOYEE_KEYWORDS
        )
        
        # Check for policy keywords
        needs_policy_data = any(
            keyword in query_lower 
            for keyword in config.POLICY_KEYWORDS
        )
        
        # If neither is clearly indicated, default to policy search
        if not needs_employee_data and not needs_policy_data:
            needs_policy_data = True
        
        return {
            'needs_employee_data': needs_employee_data,
            'needs_policy_data': needs_policy_data,
            'is_hybrid': needs_employee_data and needs_policy_data
        }
    
    def get_employee_context(self, emp_id: str, query: str) -> Optional[str]:
        """
        Get employee-specific context based on query
        
        Args:
            emp_id: Employee ID
            query: User query
            
        Returns:
            Formatted employee context string
        """
        if not emp_id:
            return None
        
        query_lower = query.lower()
        context_parts = []
        
        # Get employee info
        emp_info = self.employee_lookup.get_employee_info(emp_id)
        if not emp_info:
            return f"Employee ID {emp_id} not found in the system."
        
        # Determine what information to include
        if any(word in query_lower for word in ['leave', 'balance', 'casual', 'sick', 'earned']):
            leave_info = self.employee_lookup.get_leave_balance(emp_id)
            if leave_info:
                context_parts.append(
                    f"Leave Balance for {leave_info['Name']}:\n"
                    f"- Casual Leave: {leave_info['CasualLeave']} days\n"
                    f"- Sick Leave: {leave_info['SickLeave']} days\n"
                    f"- Earned Leave: {leave_info['EarnedLeave']} days\n"
                    f"- Total: {leave_info['TotalLeaves']} days"
                )
        
        if any(word in query_lower for word in ['manager', 'supervisor', 'boss']):
            manager_info = self.employee_lookup.get_manager_info(emp_id)
            if manager_info:
                context_parts.append(
                    f"Manager Information:\n"
                    f"- Manager Name: {manager_info['ManagerName']}\n"
                    f"- Email: {manager_info['ManagerEmail']}\n"
                    f"- Phone: {manager_info['ManagerPhone']}\n"
                    f"- Role: {manager_info['ManagerRole']}"
                )
        
        if any(word in query_lower for word in ['department', 'team', 'role']):
            dept_info = self.employee_lookup.get_department_info(emp_id)
            if dept_info:
                context_parts.append(
                    f"Department Information:\n"
                    f"- Department: {dept_info['Department']}\n"
                    f"- Role: {dept_info['Role']}\n"
                    f"- Manager: {dept_info['Manager']}\n"
                    f"- Team Size: {dept_info['TeamSize']} members\n"
                    f"- Joining Date: {dept_info['JoiningDate']}"
                )
        
        # If no specific info requested, provide basic employee info
        if not context_parts:
            context_parts.append(
                f"Employee Information:\n"
                f"- Name: {emp_info['Name']}\n"
                f"- Employee ID: {emp_info['EmpID']}\n"
                f"- Department: {emp_info['Department']}\n"
                f"- Role: {emp_info['Role']}\n"
                f"- Manager: {emp_info['Manager']}"
            )
        
        return "\n\n".join(context_parts)
    
    def get_policy_context(self, query: str) -> Optional[Dict]:
        """
        Get policy context from RAG pipeline
        
        Args:
            query: User query
            
        Returns:
            Dictionary with context and sources
        """
        if self.rag_pipeline.vector_store is None:
            return None
        
        # Retrieve relevant documents
        retrieved_docs = self.rag_pipeline.retrieve(query)
        
        if not retrieved_docs:
            return None
        
        # Format context
        context = self.rag_pipeline.format_context(retrieved_docs)
        sources = self.rag_pipeline.get_sources(retrieved_docs)
        
        return {
            'context': context,
            'sources': sources,
            'num_chunks': len(retrieved_docs)
        }
    
    def generate_response(
        self, 
        query: str, 
        emp_id: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, any]:
        """
        Generate response to user query
        
        Args:
            query: User query
            emp_id: Employee ID (optional)
            conversation_history: Previous conversation messages
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Classify query
            classification = self.classify_query(query)
            
            # Gather context
            employee_context = None
            policy_context = None
            sources = []
            
            if classification['needs_employee_data'] and emp_id:
                employee_context = self.get_employee_context(emp_id, query)
            
            if classification['needs_policy_data']:
                policy_result = self.get_policy_context(query)
                if policy_result:
                    policy_context = policy_result['context']
                    sources = policy_result['sources']
            
            # Build prompt
            prompt = self._build_prompt(
                query=query,
                employee_context=employee_context,
                policy_context=policy_context,
                conversation_history=conversation_history
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            answer = response.text
            
            # Add citations if policy data was used
            if sources:
                citations = "\n\n---\n**Sources:** " + ", ".join(sources)
                answer += citations
            
            return {
                'answer': answer,
                'sources': sources,
                'classification': classification,
                'success': True
            }
        
        except Exception as e:
            print(f"✗ Error generating response: {e}")
            return {
                'answer': f"I apologize, but I encountered an error processing your request: {str(e)}",
                'sources': [],
                'classification': {},
                'success': False
            }
    
    def _build_prompt(
        self,
        query: str,
        employee_context: Optional[str] = None,
        policy_context: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Build prompt for LLM
        
        Args:
            query: User query
            employee_context: Employee-specific context
            policy_context: Policy document context
            conversation_history: Previous messages
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        # System instruction
        prompt_parts.append(
            "You are an HR Copilot AI assistant helping employees with HR-related questions. "
            "You provide accurate, helpful, and friendly responses based on company policies "
            "and employee data. Always maintain a professional yet warm tone.\n"
        )
        
        # Add conversation history if available
        if conversation_history:
            prompt_parts.append("Previous conversation:")
            for msg in conversation_history[-4:]:  # Last 4 messages for context
                role = "User" if msg['role'] == 'user' else "Assistant"
                prompt_parts.append(f"{role}: {msg['content']}")
            prompt_parts.append("")
        
        # Add employee context
        if employee_context:
            prompt_parts.append("Employee Information:")
            prompt_parts.append(employee_context)
            prompt_parts.append("")
        
        # Add policy context
        if policy_context:
            prompt_parts.append("Relevant Policy Information:")
            prompt_parts.append(policy_context)
            prompt_parts.append("")
        
        # Add query
        prompt_parts.append(f"User Question: {query}\n")
        
        # Instructions
        prompt_parts.append(
            "Instructions:\n"
            "1. Answer the question based on the provided information\n"
            "2. Be specific and cite relevant policy details when applicable\n"
            "3. If employee data is provided, personalize the response\n"
            "4. Use a friendly, professional HR tone\n"
            "5. If you don't have enough information, say so clearly\n"
            "6. Format your response with bullet points or sections for readability\n"
            "7. Do NOT include source citations in your response (they will be added automatically)\n"
            "\nYour Response:"
        )
        
        return "\n".join(prompt_parts)
    
    def get_greeting(self, emp_id: Optional[str] = None) -> str:
        """
        Generate personalized greeting
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Greeting message
        """
        if emp_id:
            emp_info = self.employee_lookup.get_employee_info(emp_id)
            if emp_info:
                name = emp_info.get('Name', '').split()[0]  # First name
                return (
                    f"👋 Hello {name}! I'm your HR Copilot assistant.\n\n"
                    f"I can help you with:\n"
                    f"- 📋 HR policies (leave, benefits, onboarding)\n"
                    f"- 📊 Your leave balance and personal HR info\n"
                    f"- 👤 Manager and team information\n"
                    f"- ❓ Any other HR-related questions\n\n"
                    f"What would you like to know?"
                )
        
        return (
            "👋 Welcome to HR Copilot!\n\n"
            "I can help you with:\n"
            "- 📋 HR policies and procedures\n"
            "- 📊 Employee information and leave balances\n"
            "- 👤 Manager and team details\n"
            "- ❓ Any HR-related questions\n\n"
            "Please select your Employee ID from the sidebar to get personalized assistance!"
        )


# Singleton instance
_orchestrator = None

def get_orchestrator() -> LLMOrchestrator:
    """
    Get singleton instance of LLMOrchestrator
    
    Returns:
        LLMOrchestrator instance
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = LLMOrchestrator()
    return _orchestrator

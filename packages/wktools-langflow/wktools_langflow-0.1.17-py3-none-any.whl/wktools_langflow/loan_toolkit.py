"""Tool for the Loan API (get user's loan profiles)."""

from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from wktools_langflow.wrapper.loan_wrapper import LoanWrapper


class LoanQueryInput(BaseModel):
    """Input for the LoanQueryInput tool."""

    user_id: str = Field(description="user's id", default="wk")


class LoanQueryRun(BaseTool):
    """Tool for the Loan API (get user's loan profiles)."""

    name: str = "loan"
    description: str = (
        "A wrapper for loan. "
        "Useful for when you need to answer questions about current user's loans. "
        "Get user's loan profiles.")
    api_wrapper: LoanWrapper

    args_schema: Type[BaseModel] = LoanQueryInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Loan tool."""
        return self.api_wrapper.get_user_loan_profiles()



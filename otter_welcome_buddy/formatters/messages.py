class Formatter:
    """Dependency to inject messages"""

    @staticmethod
    def welcome_message() -> str:
        """Message when a new user joins the discord"""
        return "Welcome to Proyecto Nutria"

    @staticmethod
    def already_applied_message(user: str, company: str) -> str:
        """Message when the user already applied to a certain company"""
        return f"{user} already applied to {company}. ❌"

    @staticmethod
    def advanced_process_message(user: str, company: str, process_state: str) -> str:
        """Message when there is an advanced process"""
        return f"{user} has an advanced process with {company}, can't have {process_state}. ❌"

    @staticmethod
    def final_desicion_message(user: str, company: str) -> str:
        """Message when a final desicion has been made previously in the process"""
        return f"{user} has already received a desicion from {company}. ❌"

    @staticmethod
    def successful_insertion_message(
        user: str,
        company: str,
        from_offer: str,
        process_state: str,
    ) -> str:
        """Message when the insertion has been successful"""

        # if '1' there's an offer
        if from_offer == "1":
            return f"{user} has received {process_state} from {company}. 🎉"

        # if '0' there's a rejection
        if from_offer == "0":
            return f"{user} has received {process_state} from {company}. 😭"

        # there's another process
        return f"{user} has received {process_state} from {company}. ✅"

    @staticmethod
    def apply_message(user: str, company: str) -> str:
        """Message when the user has applied successfuly"""
        return f"{user} has applied to {company} successfuly. ✅"

    @staticmethod
    def proper_procedure_message(user: str, company: str) -> str:
        """Message when the user is not using the commands properly"""
        return f"{user} must apply to {company} before trying to use this command. ❌"

    @staticmethod
    def approval_message(company: str) -> str:
        """Message when a request to include a new company has been received"""
        message = f"""
        📢 Incoming Pending Approval: **{company}** for Inclusion in Our Company Portfolio. ⌛

        Please use the following commands to either accept or reject the company:

        **To Accept:** !accept [company]
        **To Reject:** !reject [company]
        """

        return message

    @staticmethod
    def company_approved_message(company: str) -> str:
        """Message when a request to include a new company has been received"""
        message = f"""
        🎉 Exciting News! {company} has been successfully accepted into our portfolio! 🚀
        """

        return message

    @staticmethod
    def company_rejected_message(company: str) -> str:
        """Message when a request to include a new company has been received"""
        message = f"""
        ❌ Unfortunately, {company} has been rejected for inclusion in our portfolio.

        *Reach out to one of our collaborators for more information.*
        """

        return message

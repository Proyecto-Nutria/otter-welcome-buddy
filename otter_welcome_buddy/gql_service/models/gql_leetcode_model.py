# pylint: skip-file
from enum import auto

from otter_welcome_buddy.gql_service.models.common import AutoEnum
from otter_welcome_buddy.gql_service.models.common import BaseGqlModel


class DifficultyOption(AutoEnum):
    """
    An enumeration representing the difficulty levels of a LeetCode problem.

    Attributes:
        All (DifficultyOption): Represents all difficulty levels.
        Easy (DifficultyOption): Represents an easy difficulty level.
        Medium (DifficultyOption): Represents a medium difficulty level.
        Hard (DifficultyOption): Represents a hard difficulty level.
    """

    All = auto()
    Easy = auto()
    Medium = auto()
    Hard = auto()


class LeetcodeQuestionCountByDifficultyModel(BaseGqlModel):
    """
    Data class representing the count of Leetcode questions by difficulty.

    Attributes:
        difficulty (DifficultyOption): The difficulty level of the Leetcode questions.
        count (int): The count of Leetcode questions for the specified difficulty.
    """

    difficulty: DifficultyOption | None = None
    count: int | None = None


class LeetcodeSubmissionCountModel(BaseGqlModel):
    """
    Data class representing the count of Leetcode submissions.

    Attributes:
        difficulty (str): The difficulty level of the submissions.
        count (int): The count of different problems where the submissions happened.
        submissions (int): The number of total submissions attempted.
    """

    difficulty: str | None = None
    count: int | None = None
    submissions: int | None = None


class LeetcodeUserSubmitStatsModel(BaseGqlModel):
    """
    Data class representing the submission statistics of a Leetcode user.

    Attributes:
        total_submission_num (list[LeetcodeSubmissionCountModel A list of total submission counts.
        ac_submission_num (list[LeetcodeSubmissionCountModel A list of accepted submission counts.
    """

    total_submission_num: list[LeetcodeSubmissionCountModel] | None = None
    ac_submission_num: list[LeetcodeSubmissionCountModel] | None = None


class LeetcodeUserContributionModel(BaseGqlModel):
    """
    Data class representing the contribution details of a Leetcode user.

    Attributes:
        points (int): The points scored by the user.
    """

    points: int | None = None


class LeetcodeUserBadgeModel(BaseGqlModel):
    """
    Data class representing the status for a Leetcode user's badge.

    Attributes:
        name (str): The name of the badge.
        expired (bool): Indicates if the badge has expired.
        hover_text (str): The text displayed when hovering over the badge.
        display_name (str): The display name of the badge.
        icon (str): The icon associated with the badge.
    """

    name: str | None = None
    expired: bool | None = None
    hover_text: str | None = None
    display_name: str | None = None
    icon: str | None = None


class LeetcodeTagProblemsCountModel(BaseGqlModel):
    """
    Data class representing the count of problems solved for a specific tag on Leetcode.

    Attributes:
        tag_name (str): The name of the tag.
        tag_slug (str): The slug identifier for the tag.
        problems_solved (int): The number of problems solved for the tag.
    """

    tag_name: str | None = None
    tag_slug: str | None = None
    problems_solved: int | None = None


class LeetcodeTagProblemCountsCategoryModel(BaseGqlModel):
    """
    Data class representing the problem counts categorized by difficulty levels for a given tag.

    Attributes:
        advanced (list[LeetcodeTagProblemsCountModel]): Problems by tag for advanced level.
        intermediate (list[LeetcodeTagProblemsCountModel]): Problems by tag for intermediate level.
        fundamental (list[LeetcodeTagProblemsCountModel]): Problems by tag for fundamental level.
    """

    advanced: list[LeetcodeTagProblemsCountModel] | None = None
    intermediate: list[LeetcodeTagProblemsCountModel] | None = None
    fundamental: list[LeetcodeTagProblemsCountModel] | None = None


class LeetcodeLanguageProblemCountModel(BaseGqlModel):
    """
    Data class representing the count of problems solved in a specific programming language.

    Attributes:
        language_name (str): The name of the programming language.
        problems_solved (int): The number of problems solved in the specified language.
    """

    language_name: str | None = None
    problems_solved: int | None = None


class LeetcodeUserProfileModel(BaseGqlModel):
    """
    Data class representing a user's profile information on Leetcode.

    Attributes:
        ranking (int): The user's ranking on Leetcode.
        user_avatar (str): The URL to the user's avatar image.
        real_name (str): The real name of the user.
        about_me (str): A brief description about the user.
        school (str): The school the user is associated with.
        websites (list[str]): A list of websites associated with the user.
        country_name (str): The name of the country the user is from.
        company (str): The company the user is working for.
        job_title (str): The job title of the user.
        skill_tags (list[str]): A list of skill tags associated with the user.
        post_view_count (int): The number of views on the user's posts.
        post_view_countDiff (int): The difference in the number of views on the user's posts.
        reputation (int): The reputation score of the user.
        reputation_diff (int): The difference in the reputation score of the user.
        solution_count (int): The number of solutions provided by the user.
        solution_countDiff (int): The difference in the number of solutions provided by the user.
        category_discuss_count (int): The number of discussions the user has participated in.
        category_discuss_count_diff (int): The difference in the number of discussions the user
                                           has participated in.
    """

    ranking: int | None = None
    user_avatar: str | None = None
    real_name: str | None = None
    about_me: str | None = None
    school: str | None = None
    websites: list[str] | None = None
    country_name: str | None = None
    company: str | None = None
    job_title: str | None = None
    skill_tags: list[str] | None = None
    post_view_count: int | None = None
    post_view_count_diff: int | None = None
    reputation: int | None = None
    reputation_diff: int | None = None
    solution_count: int | None = None
    solution_count_diff: int | None = None
    category_discuss_count: int | None = None
    category_discuss_count_diff: int | None = None


class LeetcodeUserModel(BaseGqlModel):
    """
    Data class representing a user on Leetcode.

    Attributes:
        username (str): The username of the Leetcode user.
        profile (LeetcodeUserProfileModel): The profile information of the user.
        contributions (LeetcodeUserContributionModel): The contributions made by the user.
        github_url (str): The GitHub URL of the user.
        twitter_url (str): The Twitter URL of the user.
        linkedin_url (str): The LinkedIn URL of the user.
        submission_calendar (str): JSON encoded string representing the submission calendar where
                                        each entry is a timestamp and the number of submissions.
        submit_stats_global (LeetcodeUserSubmitStatsModel): The global submission statistics of the
                                                            user.
        submit_stats (LeetcodeUserSubmitStatsModel): The submission statistics of the user.
        active_badge (LeetcodeUserBadgeModel): The active badge of the user.
        contest_badge (LeetcodeUserBadgeModel): The contest badge of the user.
        tag_problem_counts (LeetcodeTagProblemCountsCategoryModel): The problem counts categorized
                                                                    by tags.
        language_problem_count (list[LeetcodeLanguageProblemCountModel]): The problem counts
                                                        categorized by programming languages.
        is_discuss_admin (bool): Indicates if the user is a discuss admin.
        is_discuss_staff (bool): Indicates if the user is a discuss staff member.
        is_active (bool): Indicates if the user is currently active.
    """

    username: str | None = None
    profile: LeetcodeUserProfileModel | None = None
    contributions: LeetcodeUserContributionModel | None = None
    github_url: str | None = None
    twitter_url: str | None = None
    linkedin_url: str | None = None
    # Encode JSON object where each entry represent:
    # {
    #   timestamp: # submissions
    # }
    submission_calendar: str | None = None
    submit_stats_global: LeetcodeUserSubmitStatsModel | None = None
    submit_stats: LeetcodeUserSubmitStatsModel | None = None
    active_badge: LeetcodeUserBadgeModel | None = None
    contest_badge: LeetcodeUserBadgeModel | None = None
    tag_problem_counts: LeetcodeTagProblemCountsCategoryModel | None = None
    language_problem_count: list[LeetcodeLanguageProblemCountModel] | None = None
    is_discuss_admin: bool | None = None
    is_discuss_staff: bool | None = None
    is_active: bool | None = None


class LeetcodeLevelBeatPercentageMixinModel(BaseGqlModel):
    """
    Data class representing the percentage of users who have beaten a certain difficulty level.

    Attributes:
        difficulty (str): The difficulty level of the LeetCode problem (e.g., 'Easy').
        percentage (int): The percentage of users who have beaten the problems at the given level
    """

    difficulty: str | None = None
    percentage: int | None = None


class LeetcodeQuestionCountModel(BaseGqlModel):
    """
    Data class representing the count of Leetcode questions and their associated difficulty level.

    Attributes:
        count (int): The number of Leetcode questions.
        difficulty (str): The difficulty level of the questions.
    """

    count: int | None = None
    difficulty: str | None = None


class LeetcodeUserQuestionProgressModel(BaseGqlModel):
    """
    Data class representing the progress of a Leetcode user in terms of their
    question-solving statistics.

    Attributes:
        num_accepted_questions (list[LeetcodeQuestionCountModel]): The count of accepted questions
                                                                   by difficulty.
        num_failed_questions (list[LeetcodeQuestionCountModel]): The count of failed questions by
                                                                 difficulty.
        num_untouched_questions (list[LeetcodeQuestionCountModel]): The count of untouched questions
                                                                    by difficulty.
        user_session_beats_percentage (list[LeetcodeLevelBeatPercentageMixinModel]): The user's
                                                        session beats percentage by difficulty.
    """

    num_accepted_questions: list[LeetcodeQuestionCountModel] | None = None
    num_failed_questions: list[LeetcodeQuestionCountModel] | None = None
    num_untouched_questions: list[LeetcodeQuestionCountModel] | None = None
    user_session_beats_percentage: list[LeetcodeLevelBeatPercentageMixinModel] | None = None


class LeetcodePostModel(BaseGqlModel):
    """
    Data class representing a post on Leetcode with various attributes.

    Attributes:
        id (str): The unique identifier of the post.
        vote_status (int): The vote status of the post.
        vote_count (int): The number of votes the post has received.
        content (str): The content of the post.
        creation_date (int): The timestamp of when the post was created.
        updation_date (int): The timestamp of the last update to the post.
        status (str): The status of the post.
        is_hidden (bool): Indicates if the post is hidden.
        author (LeetcodeUserModel): The author of the post.
        author_is_moderator (bool): Indicates if the author is a moderator.
        is_own_post (bool): Indicates if the post is authored by the current user.
    """

    id: str | None = None
    vote_status: int | None = None
    vote_count: int | None = None
    content: str | None = None
    creation_date: int | None = None
    updation_date: int | None = None
    status: str | None = None
    is_hidden: bool | None = None
    author: LeetcodeUserModel | None = None
    author_is_moderator: bool | None = None
    is_own_post: bool | None = None


class LeetcodeSolutionTagModel(BaseGqlModel):
    """
    Data class representing a tag associated with a Leetcode solution.

    Attributes:
        name (str): The name of the tag.
        slug (str): The slug (URL-friendly version) of the tag.
        count (int): The count of occurrences of this tag.
    """

    name: str | None = None
    slug: str | None = None
    count: int | None = None


class LeetcodeTopicModel(BaseGqlModel):
    """
    Data class representing a topic on Leetcode with various attributes.

    Attributes:
        id (str): The unique identifier of the topic.
        view_count (int): The number of views the topic has received.
        comment_count (int): The total number of comments on the topic.
        top_level_comment_count (int): The number of top-level comments on the topic.
        subscribed (bool): Indicates if the user is subscribed to the topic.
        title (str): The title of the topic.
        pinned (bool): Indicates if the topic is pinned.
        solution_tags (list[LeetcodeSolutionTagModel]): A list of solution tags associated with
                                                        the topic.
        hide_from_trending (bool): Indicates if the topic should be hidden from trending lists.
        is_favorite (bool): Indicates if the topic is marked as a favorite by the user.
        post (LeetcodePostModel): The post associated with the topic.
    """

    id: str | None = None
    view_count: int | None = None
    comment_count: int | None = None
    top_level_comment_count: int | None = None
    subscribed: bool | None = None
    title: str | None = None
    pinned: bool | None = None
    solution_tags: list[LeetcodeSolutionTagModel] | None = None
    hide_from_trending: bool | None = None
    is_favorite: bool | None = None
    post: LeetcodePostModel | None = None


class LeetcodeTopicTagModel(BaseGqlModel):
    """
    Data class representing a Leetcode topic tag.

    Attributes:
        id (str): The unique identifier of the topic tag.
        name (str): The name of the topic tag.
        slug (str): The slug of the topic tag.
    """

    id: str | None = None
    name: str | None = None
    slug: str | None = None


class LeetcodeSubmissionDumpModel(BaseGqlModel):
    """
    Data class representing a Leetcode submission.

    Attributes:
        id (str): The unique identifier of the submission.
        title (str): The title of the submission.
        title_slug (str): The slugified title of the submission.
        timestamp (int): The timestamp of the submission.
        runtime (str): The runtime of the submission.
        memory (str): The memory usage of the submission.
        status (int): The status code of the submission.
        status_display (str): The display status of the submission.
        lang (str): The programming language used in the submission.
        lang_name (str): The full name of the programming language used in the submission.
        url (str): The URL of the submission.
        is_pending (str): Indicates if the submission is pending.
        has_notes (bool): Indicates if the submission has notes.
        notes (str): The notes associated with the submission.
        flag_type (str): The flag type of the submission.
        topic_tags (list[LeetcodeTopicTagModel]): The topic tags associated with the submission.
    """

    id: str | None = None
    title: str | None = None
    title_slug: str | None = None
    timestamp: int | None = None
    runtime: str | None = None
    memory: str | None = None
    status: int | None = None
    status_display: str | None = None
    lang: str | None = None
    lang_name: str | None = None
    url: str | None = None
    is_pending: str | None = None
    has_notes: bool | None = None
    notes: str | None = None
    flag_type: str | None = None
    topic_tags: list[LeetcodeTopicTagModel] | None = None


class LeetcodeLanguageModel(BaseGqlModel):
    """
    Data class representing a language model for Leetcode.

    Attributes:
        id (str): The unique identifier of the language model.
        name (str): The name of the language model.
    """

    id: str | None = None
    name: str | None = None


class LeetcodeUserRatingModel(BaseGqlModel):
    """
    Data class representing the rating model for a Leetcode user.

    Attributes:
        score (int): The score of the Leetcode user. Defaults to None.
    """

    score: int | None = None


class LeetcodeRatingModel(BaseGqlModel):
    """
    Data class representing the rating model for Leetcode.

    Attributes:
        count (int): The count of ratings.
        average (str): The average rating as a string.
        user_rating (LeetcodeUserRatingModel): The user rating model.
    """

    count: int | None = None
    average: str | None = None
    user_rating: LeetcodeUserRatingModel | None = None


class LeetcodeArticleModel(BaseGqlModel):
    """
    LeetcodeArticleModel represents the structure of a Leetcode article.

    Attributes:
        id (str): The unique identifier of the article.
        title (str): The title of the article.
        content (str): The content of the article.
        content_type_id (str): The type identifier of the content.
        paid_only (bool): Indicates if the article is for paid users only.
        has_video_solution (bool): Indicates if the article has a video solution.
        paid_only_video (bool): Indicates if the video solution is for paid users only.
        can_see_detail (bool): Indicates if the user can see the detailed content.
        rating (LeetcodeRatingModel): The rating of the article.
        topic (LeetcodeTopicModel): The topic of the article.
    """

    id: str | None = None
    title: str | None = None
    content: str | None = None
    content_type_id: str | None = None
    paid_only: bool | None = None
    has_video_solution: bool | None = None
    paid_only_video: bool | None = None
    can_see_detail: bool | None = None
    rating: LeetcodeRatingModel | None = None
    topic: LeetcodeTopicModel | None = None


class LeetcodeCodeSnippetModel(BaseGqlModel):
    """
    Data class representing a code snippet in LeetCode.

    Attributes:
        lang (str): The programming language of the code snippet.
        lang_slug (str): The slug identifier for the programming language.
        code (str): The actual code snippet used as a template in the code editor.
    """

    lang: str | None = None
    lang_slug: str | None = None
    # String used as template in the code editor
    code: str | None = None


class LeetcodeQuestionModel(BaseGqlModel):
    """
    LeetcodeQuestionModel represents the data model for a Leetcode question.

    Attributes:
        question_id (str): The unique identifier for the question.
        question_frontend_id (str): The frontend identifier for the question.
        title (str): The title of the question.
        title_slug (str): The slugified title of the question.
        translated_title (str): The translated title of the question.
        category_title (str): The category title of the question.
        is_favor (bool): Indicates if the question is marked as favorite.
        is_paid_only (bool): Indicates if the question is paid-only.
        hide (bool): Indicates if the question is hidden.
        ac_rate (int): The acceptance rate of the question.
        difficulty (str): The difficulty level of the question.
        content (str): The content of the question in HTML format.
        stats (str): The statistics of the question encoded in JSON format.
        hints (list[str The list of hints for the question in HTML format.
        mysql_schemas (list[str The list of SQL schemas used in database problems.
        data_schemas (list[str The list of Pandas schemas used in database problems.
        status (str): The status of the question, e.g., "ac", null when no submission.
        has_solution (bool): Indicates if the question has a solution.
        has_video_solution (bool): Indicates if the question has a video solution.
        solution (LeetcodeArticleModel): The solution article for the question.
        topic_tags (list[LeetcodeTopicTagModel The list of topic tags associated with the question.
        similar_question_list (list["LeetcodeQuestionModel" The list of similar questions.
        likes (int): The number of likes for the question.
        dislikes (int): The number of dislikes for the question.
        code_snippets (list[LeetcodeCodeSnippetModel The list of code snippets for the question.
        can_see_question (bool): Indicates if the question can be seen.
        env_info (str): The environment information for the question.
        has_frontend_preview (bool): Indicates if the question has a frontend preview.
        frontend_previews (str): The frontend previews for the question.
        enable_debugger (bool): Indicates if the debugger is enabled for the question.
        enable_run_code (bool): Indicates if running code is enabled for the question.
        enable_submit (bool): Indicates if submitting code is enabled for the question.
        enable_test_mode (bool): Indicates if test mode is enabled for the question.
        example_testcase_list (list[str The list of example test cases for the question.
        metaData (str): The metadata for the question encoded in JSON format.
    """

    question_id: str | None = None
    question_frontend_id: str | None = None
    title: str | None = None
    title_slug: str | None = None
    translated_title: str | None = None
    category_title: str | None = None
    is_favor: bool | None = None
    is_paid_only: bool | None = None
    hide: bool | None = None
    ac_rate: int | None = None
    difficulty: str | None = None
    # Str in html format to be displayed in the browser
    content: str | None = None
    # Encode JSON in format:
    # {
    #   totalAccepted: str,
    #   totalSubmission: str,
    #    totalAcceptedRaw: Optional[int] = None,
    #    totalSubmissionRaw: Optional[int] = None,
    #    acRate: str
    # }
    stats: str | None = None
    # Hints sorted, the first hint is the easiest one,
    # is a str in html format
    hints: list[str] | None = None
    # SQL schema used in database problems
    mysql_schemas: list[str] | None = None
    # Pandas schema used in database problems
    data_schemas: list[str] | None = None
    # freqBar
    # eg: "ac", null when no submission
    status: str | None = None
    has_solution: bool | None = None
    has_video_solution: bool | None = None
    solution: LeetcodeArticleModel | None = None
    topic_tags: list[LeetcodeTopicTagModel] | None = None
    similar_question_list: list["LeetcodeQuestionModel"] | None = None
    likes: int | None = None
    dislikes: int | None = None
    code_snippets: list[LeetcodeCodeSnippetModel] | None = None
    can_see_question: bool | None = None
    env_info: str | None = None
    has_frontend_preview: bool | None = None
    frontend_previews: str | None = None
    enable_debugger: bool | None = None
    enable_run_code: bool | None = None
    enable_submit: bool | None = None
    enable_test_mode: bool | None = None
    # Examples split by \n, they should match the metadata description
    example_testcase_list: list[str] | None = None
    # Encode JSON in format:
    # {
    #   'name': str,
    #   'params': [{
    #     'name': str,
    #     'type': str
    #   }],
    #   'return': {
    #     'type': str
    #   }
    # }
    metaData: str | None = None


class LeetcodePagifiedQuestionModel(BaseGqlModel):
    """
    Data class representing a paginated list of Leetcode questions.

    Attributes:
        total_num (int): The total number of questions.
        data (list[LeetcodeQuestionModel]): A list of LeetcodeQuestionModel instances.
    """

    total_num: int | None = None
    data: list[LeetcodeQuestionModel] | None = None


class LeetcodeCommonTagModel(BaseGqlModel):
    """
    Data class representing a common tag in Leetcode.

    Attributes:
        name (str): The name of the tag.
        slug (str): The slug identifier for the tag.
    """

    name: str | None = None
    slug: str | None = None


class LeetcodePanelQuestionModel(BaseGqlModel):
    """
    Data class representing a Leetcode question panel.

    Attributes:
        difficulty (str): The difficulty level of the question (e.g., "Easy", "Medium", "Hard").
        id (str): The unique identifier for the question.
        paid_only (bool): Indicates if the question is available only for paid users.
        question_frontend_id (str): The frontend ID of the question.
        status (str): The status of the question (e.g., "Solved", "Unsolved").
        title (str): The title of the question.
        title_slug (str): The slugified title of the question.
        score (int): The score of the question.
        question_number (int): The number of the question.
    """

    difficulty: str | None = None
    id: str | None = None
    paid_only: bool | None = None
    question_frontend_id: str | None = None
    status: str | None = None
    title: str | None = None
    title_slug: str | None = None
    score: int | None = None
    question_number: int | None = None


class LeetcodePanelQuestionListModel(BaseGqlModel):
    """
    Data class representing a list of Leetcode panel questions.

    Attributes:
        has_view_permission (bool): Indicates if the user has permission to view the panel.
        panel_name (str): The name of the panel.
        finished_length (int): The number of questions that have been finished.
        total_length (int): The total number of questions in the panel.
        questions (list[LeetcodePanelQuestionModel]): A list of Leetcode panel questions.
    """

    has_view_permission: bool | None = None
    panel_name: str | None = None
    finished_length: int | None = None
    total_length: int | None = None
    questions: list[LeetcodePanelQuestionModel] | None = None


class LeetcodeDailyChallengeModel(BaseGqlModel):
    """
    Data class representing a daily Leetcode challenge.

    Attributes:
        date (str): The date of the daily challenge.
        user_status (str): The status of the user for the daily challenge.
        link (str): The link to the daily challenge.
        question (LeetcodeQuestionModel): The question associated with the daily challenge.
    """

    date: str | None = None
    user_status: str | None = None
    link: str | None = None
    question: LeetcodeQuestionModel | None = None


class LeetcodeCodingChallengeModel(BaseGqlModel):
    """
    Data class representing the GraphQL model for Leetcode coding challenges.

    Attributes:
        challenges (list[LeetcodeDailyChallengeModel]): A list of daily Leetcode challenges.
        weekly_challenges (list[LeetcodeDailyChallengeModel]): A list of weekly Leetcode challenges.
    """

    challenges: list[LeetcodeDailyChallengeModel] | None = None
    weekly_challenges: list[LeetcodeDailyChallengeModel] | None = None

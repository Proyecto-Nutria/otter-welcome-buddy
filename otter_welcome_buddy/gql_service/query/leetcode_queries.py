USER_PROFILE_QUERY: str = """
query userPublicProfile($username: String!) {
    matchedUser(username: $username) {
        username
        profile {
            countryName
            ranking
            userAvatar
        }
    }
}
"""

ACTIVE_DAILY_CHALLENGE_QUERY: str = """
query activeDailyChallenge {
    activeDailyCodingChallengeQuestion {
      date
      link
      question {
        title
        difficulty
        categoryTitle
        topicTags {
          name
        }
      }
    }
}
"""

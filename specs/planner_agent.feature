Feature: Planner Agent
  As a student with an upcoming exam
  I want a personalized study schedule
  So that I can cover all topics before my exam date

  Scenario: Generate study plan
    Given the student provides subject "DBMS"
    And exam date is 7 days away
    When the Planner agent receives the request
    Then it returns a day-by-day study schedule
    And each day has specific topics and time estimates
    And weak topics from Tracker agent are given priority
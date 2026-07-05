Feature: Quiz Agent
  As a college student
  I want to be quizzed on any topic
  So that I can test my understanding and track weak areas

  Scenario: Generate MCQ quiz on a topic
    Given the student enters "Operating Systems" as the topic
    And selects "Medium" difficulty
    When the Quiz agent receives the request
    Then it returns 5 multiple choice questions
    And each question has 4 options and a correct answer index
    And each question includes an explanation

  Scenario: Adaptive difficulty
    Given the student has scored below 60% on previous quizzes
    When the Tracker agent detects weak performance
    Then the Quiz agent increases difficulty on next attempt
Feature: Teaching Agent
  As a college student
  I want concepts explained clearly with examples
  So that I can understand difficult topics without a human tutor

  Scenario: Explain a concept with analogy
    Given the student asks "explain binary search trees"
    When the Teaching agent receives the request
    Then it returns a structured explanation with definition
    And includes a real-world analogy to simplify the concept
    And suggests related topics to study next

  Scenario: Socratic Mode questioning
    Given the student enters "Operating Systems" as the topic
    And selects "Socratic Mode"
    When the Teaching agent starts a Socratic session
    Then it asks the student a question instead of explaining
    And evaluates the student answer as Correct, Partial, or Wrong
    And provides feedback and explanation only after the answer
    And continues for 5 questions before showing a final score

  Scenario: Formula Sheet generation
    Given the student enters "DBMS" as the topic
    When the Teaching agent receives a formula sheet request
    Then it returns 8 to 14 key concepts with formulas and descriptions
    And each concept includes a brief example
    And the output is structured and easy to revise from
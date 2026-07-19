Feature: Step given a request form-data payload
    Validates the functionality of the given step "a request form-data payload"


    Scenario: Sets the specified form-data payload in the context
        Given a request form-data payload
            | key        | value                    | type |
            | timesheet  | features/files/test.csv  | file |
            | projectId  | 123                      | text |
        Then the context contains request form-data file timesheet with value set to features/files/test.csv
            And the context contains request form-data text projectId with value set to 123

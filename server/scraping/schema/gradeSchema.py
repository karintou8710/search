# 新課程成績のjson schema
gradeJsonSchema = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "model",
            "fields"
        ],
        "properties": {
            "model": {
                "type": "string",
                "pattern": "^api.gradeinfo$"
            },
            "fields": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "subject",
                    "lecture",
                    "group",
                    "teacher",
                    "year",
                    "semester",
                    "faculty",
                    "numOfStudents",
                    "ap",
                    "a",
                    "am",
                    "bp",
                    "b",
                    "bm",
                    "cp",
                    "c",
                    "d",
                    "dm",
                    "f",
                    "gpa"
                ],
                "properties": {
                    "subject": {
                        "type": "string",
                        "maxLength": 100
                    },
                    "lecture": {
                        "type": "string",
                        "maxLength": 100
                    },
                    "group": {
                        "type": "string",
                        "maxLength": 100
                    },
                    "teacher": {
                        "type": "string",
                        "maxLength": 100
                    },
                    "year": {
                        "type": "string",
                        "pattern": "^\\d{4}$"
                    },
                    "semester": {
                        "type": "string",
                        "pattern": "^(1|2)学期$"
                    },
                    "faculty": {
                        "type": "string",
                        "maxLength": 100
                    },
                    "numOfStudents": {
                        "type": "integer"
                    },
                    "ap": {
                        "type": "integer"
                    },
                    "a": {
                        "type": "integer"
                    },
                    "am": {
                        "type": "integer"
                    },
                    "bp": {
                        "type": "integer"
                    },
                    "b": {
                        "type": "integer"
                    },
                    "bm": {
                        "type": "integer"
                    },
                    "cp": {
                        "type": "integer"
                    },
                    "c": {
                        "type": "integer"
                    },
                    "d": {
                        "type": "integer"
                    },
                    "dm": {
                        "type": "integer"
                    },
                    "f": {
                        "type": "integer"
                    },
                    "gpa": {
                        "type": "number"
                    }
                }
            }
        }
    }
}

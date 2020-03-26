from enum import Enum


class Commands(Enum):
    CREATOR: str = "creator"
    USERS: str = "users"
    METRICS: str = "metrics"
    DATA: str = "data"
    CLEAR: str = "clear"
    ERASE: str = "erase"
    DROP: str = "drop"
    GUARDDROP: str = "guarddrop"
    BROADCAST: str = "broadcast"
    POLL: str = "poll"
    REVERSE: str = "reverse"
    DAYOFF: str = "dayoff"
    
    CANCEL: str = "cancel"
    START: str = "start"
    
    LOGIN: str = "login"
    LOGIN_EXTENDED: str = "login-extended"
    LOGIN_COMPACT: str = "login-сompact"
    LOGIN_SET_INSTITUTE: str = "login-set-institute-"
    LOGIN_SET_YEAR: str = "login-set-year-"
    LOGIN_SET_GROUP: str = "login-set-group-"
    LOGIN_SET_NAME: str = "login-set-name-"
    LOGIN_SET_CARD: str = "login-set-card"
    UNLOGIN: str = "un-login"
    
    CLASSES: str = "classes"
    EXAMS: str = "exams"
    
    LECTURERS: str = "lecturers"
    LECTURERS_NAME: str = "lecturers-name"
    
    SCORE: str = "score"
    SCORE_SEMESTER: str = "score-semester"
    SCORE_ALL: str = "score-all"
    SCORE_EXAMS: str = "score-exams"
    SCORE_TESTS: str = "score-test"
    SCORE_GRADED_TESTS: str = "score-graded-test"
    
    NOTES: str = "notes"
    NOTES_ADD: str = "notes-add"
    NOTES_SHOW: str = "notes-show"
    NOTES_SHOW_ALL: str = "notes-show-all"
    NOTES_DELETE: str = "notes-delete"
    NOTES_DELETE_ALL: str = "notes-delete-all"
    
    EDIT: str = "edit"
    EDIT_ADD: str = "edit-add"
    EDIT_WEEKTYPE: str = "edit-weektype"
    EDIT_WEEKDAY: str = "edit-weekday"
    EDIT_HOUR: str = "edit-hour"
    EDIT_TIME: str = "edit-time"
    EDIT_BUILDING: str = "edit-building"
    EDIT_AUDITORIUM: str = "edit-auditorium"
    EDIT_SUBJECT_TITLE: str = "edit-subject-title"
    EDIT_SUBJECT_TYPE: str = "edit-subject-title"
    EDIT_LECTURER: str = "edit-lecturer-name"
    EDIT_DEPARTMENT: str = "edit-department"
    EDIT_SHOW: str = "edit-show"
    EDIT_SHOW_ALL: str = "edit-show-all"
    EDIT_SHOW_WEEKTYPE: str = "edit-show-weektype"
    EDIT_SHOW_WEEKDAY: str = "edit-show-weekday"
    EDIT_SHOW_EDIT: str = "edit-show-edit"
    EDIT_DELETE: str = "edit-delete"
    EDIT_DELETE_ALL: str = "edit-delete-all"
    EDIT_DELETE_WEEKTYPE: str = "edit-delete-weektype"
    EDIT_DELETE_WEEKDAY: str = "edit-delete-weekday"
    EDIT_DELETE_EDIT: str = "edit-delete-edit"
    
    LOCATIONS: str = "locations"
    
    WEEK: str = "week"
    BRS: str = "brs"
    HELP: str = "help"
    DONATE: str = "donate"
    
    SETTINGS: str = "settings"
    SETTINGS_APPEARANCE: str = "settings-appearance"
    SETTINGS_APPEARANCE_DONE: str = "settings-appearance-done"
    SETTINGS_APPEARANCE_DROP: str = "settings-appearance-drop"
    
    UNKNOWN_NONTEXT_MESSAGE: str = "unknown-nontext-message"
    UNKNOWN_TEXT_MESSAGE: str = "unknown-text-message"
    UNKNOWN_CALLBACK: str = "unknown-callback"

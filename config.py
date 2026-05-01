"""Configuration constants for the header scanner."""

TIMEOUT = 10

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Permissions-Policy",
    "Referrer-Policy",  
]    

# This variables are going to be used for the max-age on the Strict-Transport-Security so I can work with the number I get from the header and give a good report
ONE_YEAR_IN_SECONDS = 31536000      
SIX_MONTHS_IN_SECONDS = 15768000   
ONE_MONTH_IN_SECONDS = 2592000      

# This list is used on the Permissions-Policy Header and its so I can look up the features we can have on this header easily 
# This features are mainly what our websites can have access
SENSITIVE_FEATURES = {
    "camera", "microphone", "geolocation",
    "usb", "serial", "hid", "bluetooth",
    "payment", "accelerometer", "gyroscope",
    "magnetometer", "midi", "display-capture",
}
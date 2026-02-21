import os
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def bridge():
    # קבלת הפרמטר שימות המשיח שולחת (הקוד שהמאזין הקיש)
    user_input = request.args.get('val_name')
    
    if not user_input:
        return "read=t-נא להקיש קוד שיר"

    # כתובת ה-API שלך (החלף בקישור האמיתי שיש לך אם הוא שונה)
    # אם יש לך מפתח API, הוסף אותו כאן במקום ה-API_KEY
    api_url = f"https://tubeapi.org/api/v1/download?id={user_input}"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        # אנחנו מחפשים שדה בשם 'link' או 'url' בתשובה מה-API
        song_link = data.get('link') or data.get('url')
        
        if song_link:
            return f"play_url={song_link}"
        else:
            return "read=t-השיר לא נמצא במערכת"
            
    except Exception as e:
        return "read=t-חלה שגיאה בתקשורת עם השרת"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

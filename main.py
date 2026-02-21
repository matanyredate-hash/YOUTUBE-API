from flask import Flask, request
import requests

app = Flask(__name__)

# פונקציה שתופסת את כל סוגי הכתובות כדי למנוע שגיאת Not Found
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def bridge(path):
    # שליפת הפרמטר שימות המשיח שולחת (מה שהמשתמש הקיש בטלפון)
    user_input = request.args.get('val_name')
    
    # הודעת בדיקה למקרה שנכנסים לדף בלי להקיש קוד שיר
    if not user_input:
        return "השרת מחובר בהצלחה! נא להוסיף ?val_name=ID לכתובת כדי לבדוק שיר."

    # כתובת ה-API החיצונית - כאן מתבצעת הפנייה להורדה
    # וודא שזו הכתובת המדויקת שקיבלת מהספק
    api_url = f"https://tubeapi.org/api/v1/download?id={user_input}"
    
    try:
        # פנייה לשרת ה-API עם המתנה של מקסימום 10 שניות
        response = requests.get(api_url, timeout=10)
        
        # אם השרת החזיר תשובה תקינה
        if response.status_code == 200:
            data = response.json()
            
            # ניסיון לשלוף את הלינק מתוך התשובה (בודק כמה שמות אפשריים)
            song_link = data.get('link') or data.get('url') or data.get('download_url')
            
            if song_link:
                # מחזיר לימות המשיח פקודה לנגן את הלינק שנמצא
                return f"play_url={song_link}"
            else:
                return "read=t-השיר לא נמצא במאגר ה-API"
        else:
            return f"read=t-שגיאה מהשרת החיצוני קוד {response.status_code}"
            
    except Exception as e:
        # במקרה של תקלה טכנית בחיבור
        return f"read=t-חלה שגיאה בתקשורת: {str(e)}"

if __name__ == "__main__":
    # הגדרת הפורט המתאים ל-Render
    app.run(host='0.0.0.0', port=10000)

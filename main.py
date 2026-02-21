from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def bridge(path):
    user_input = request.args.get('val_name')
    
    if not user_input:
        return "Server is Live! Please provide a video ID using ?val_name="

    # כתובת ה-API החדשה שביקשת
    # הערה: ייתכן שהמערכת הזו דורשת מזהה וידאו (slug) ולא לינק מלא
    api_url = f"https://tube.switch.ch/api/v1/videos/{user_input}"
    
    try:
        # פנייה ל-API של Switch Tube
        # בדרך כלל דרוש כאן אישור (Token), ננסה גישה ציבורית קודם
        r = requests.get(api_url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            # במערכת הזו הלינק נמצא בדרך כלל תחת שדה שנקרא download_url או video_url
            link = data.get('download_url') or data.get('video_url')
            
            if link:
                return f"play_url={link}"
            else:
                return "read=t-הסרטון נמצא אך לא נמצא קישור להורדה"
        elif r.status_code == 401:
            return "read=t-חסרה הרשאה לגשת לשרת הזה"
        else:
            return f"read=t-שגיאה מהשרת קוד {r.status_code}"
            
    except Exception as e:
        return f"read=t-תקלה בחיבור: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

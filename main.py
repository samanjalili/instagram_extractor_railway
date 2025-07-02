from flask import Flask, render_template, request, send_file
import instaloader
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    file_ready = False
    error = None

    if request.method == 'POST':
        login_user = request.form['login_username']
        login_pass = request.form['login_password']
        target_username = request.form['target_username']

        try:
            L = instaloader.Instaloader()

            # استفاده از پروکسی رایگان تستی
            L.context.proxy = "http://194.170.146.125:8080"

            # لاگین به اینستاگرام
            L.login(login_user, login_pass)

            # دریافت پروفایل پیج هدف
            profile = instaloader.Profile.from_username(L.context, target_username)
            followers = list(profile.get_followers())
            followings = list(profile.get_followees())

            # ذخیره در فایل
            os.makedirs('output', exist_ok=True)
            with open('output/result.txt', 'w', encoding='utf-8') as f:
                f.write(f'🔹 تعداد فالورها: {len(followers)}\n')
                f.write(f'🔹 تعداد فالووینگ‌ها: {len(followings)}\n\n')
                f.write('🔸 لیست یوزرنیم‌های فالورها:\n')
                for user in followers[:100]:
                    try:
                        f.write(f" - {user.username} 🔹 فالوورها: {user.followers} | فالووینگ‌ها: {user.followees}\n")
                    except:
                        f.write(f" - {user.username} 🔹 اطلاعات در دسترس نیست\n")

            file_ready = True

        except Exception as e:
            error = str(e)

    return render_template('index.html', file_ready=file_ready, error=error)

@app.route('/download')
def download():
    return send_file('output/result.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

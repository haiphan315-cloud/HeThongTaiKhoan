from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# BỘ DỮ LIỆU TÀI KHOẢN KẾ TOÁN (Dữ liệu mẫu theo TT 200)
# Bạn có thể tự thêm các tài khoản khác vào đây theo cú pháp: "Số TK": "Tên TK",
ACCOUNT_DATA = {
    "111": "Tiền mặt",
    "1111": "Tiền Việt Nam",
    "1112": "Ngoại tệ",
    "1113": "Vàng tiền tệ",
    "112": "Tiền gửi ngân hàng",
    "1121": "Tiền Việt Nam",
    "1122": "Ngoại tệ",
    "121": "Chứng khoán kinh doanh",
    "131": "Phải thu của khách hàng",
    "133": "Thuế GTGT được khấu trừ",
    "141": "Tạm ứng",
    "152": "Nguyên liệu, vật liệu",
    "153": "Công cụ, dụng cụ",
    "156": "Hàng hóa",
    "211": "Tài sản cố định hữu hình",
    "214": "Hao mòn tài sản cố định",
    "331": "Phải trả cho người bán",
    "333": "Thuế và các khoản phải nộp Nhà nước",
    "334": "Phải trả người lao động",
    "338": "Phải trả, phải nộp khác",
    "411": "Vốn đầu tư của chủ sở hữu",
    "421": "Lợi nhuận sau thuế chưa phân phối",
    "511": "Doanh thu bán hàng và cung cấp dịch vụ",
    "632": "Giá vốn hàng bán",
    "641": "Chi phí bán hàng",
    "642": "Chi phí quản lý doanh nghiệp",
    "711": "Thu nhập khác",
    "811": "Chi phí khác",
    "911": "Xác định kết quả kinh doanh"
}

# GIAO DIỆN HTML WEB CHAT
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tra cứu Tài khoản Kế toán</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
        .chat-container { width: 100%; max-width: 500px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; }
        .chat-header { background: #10ac84; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; }
        .chat-box { height: 450px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: #fafafa; }
        .msg { max-width: 85%; padding: 10px 15px; border-radius: 20px; font-size: 15px; line-height: 1.5; }
        .user-msg { background: #10ac84; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot-msg { background: #e4e6eb; color: black; align-self: flex-start; border-bottom-left-radius: 2px; }
        .input-area { display: flex; padding: 10px; background: white; border-top: 1px solid #ddd; }
        input { flex: 1; padding: 10px 15px; border: 1px solid #ccc; border-radius: 20px; outline: none; font-size: 15px; }
        button { background: #10ac84; color: white; border: none; padding: 10px 20px; margin-left: 10px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        button:hover { background: #01a3a4; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">Bot Tra Cứu Kế Toán</div>
    <div class="chat-box" id="chat-box">
        <div class="msg bot-msg">Chào bạn! Nhập số tài khoản hoặc tên tài khoản cần tra cứu vào đây nhé.</div>
    </div>
    <div class="input-area">
        <input type="text" id="user-input" placeholder="Ví dụ: 111 hoặc Tiền mặt..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Tra cứu</button>
    </div>
</div>

<script>
    function handleKeyPress(e) {
        if (e.keyCode === 13) sendMessage();
    }

    async function sendMessage() {
        const inputField = document.getElementById('user-input');
        const message = inputField.value.trim();
        if (!message) return;

        const chatBox = document.getElementById('chat-box');
        
        chatBox.innerHTML += `<div class="msg user-msg">${message}</div>`;
        inputField.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            
            // Xử lý xuống dòng cho đẹp
            const formattedReply = data.reply.replace(/\\n/g, '<br>');
            chatBox.innerHTML += `<div class="msg bot-msg">${formattedReply}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            chatBox.innerHTML += `<div class="msg bot-msg">Hệ thống đang bận, vui lòng thử lại!</div>`;
        }
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get("message", "").strip().lower()
    
    # 1. Nếu người dùng nhập CHÍNH XÁC số tài khoản
    if user_query in ACCOUNT_DATA:
        bot_reply = f"Tài khoản {user_query} là: {ACCOUNT_DATA[user_query]}"
        return jsonify({"reply": bot_reply})
        
    # 2. Nếu người dùng nhập TỪ KHÓA (tìm kiếm tương đối)
    results = []
    for acc_num, acc_name in ACCOUNT_DATA.items():
        # Tìm trong cả số tài khoản hoặc tên tài khoản
        if user_query in acc_name.lower() or user_query in acc_num:
            results.append(f"• TK {acc_num}: {acc_name}")
            
    if results:
        bot_reply = "Kết quả tìm kiếm:\\n" + "\\n".join(results)
    else:
        bot_reply = "Không tìm thấy tài khoản nào khớp với dữ liệu bạn nhập."
        
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
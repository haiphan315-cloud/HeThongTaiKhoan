from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# BỘ DỮ LIỆU TÀI KHOẢN KẾ TOÁN (Đã cập nhật full data của bạn)
ACCOUNT_DATA = {
    "111": "Tiền mặt",
    "112": "Tiền gửi không kỳ hạn",
    "113": "Tiền đang chuyển",
    "121": "Chứng khoán kinh doanh",
    "128": "Đầu tư nắm giữ đến ngày đáo hạn",
    "1281": "Tiền gửi có kỳ hạn",
    "1282": "Trái phiếu",
    "1283": "Cho vay",
    "1288": "Các khoản đầu tư khác nắm giữ đến ngày đáo hạn",
    "131": "Phải thu của khách hàng",
    "133": "Thuế GTGT được khấu trừ",
    "1331": "Thuế GTGT được khấu trừ của hàng hóa, dịch vụ",
    "1332": "Thuế GTGT được khấu trừ của TSCĐ",
    "136": "Phải thu nội bộ",
    "1361": "Vốn kinh doanh ở đơn vị trực thuộc",
    "1362": "Phải thu nội bộ về chênh lệch tỷ giá",
    "1363": "Phải thu nội bộ về chi phí đi vay đủ điều kiện được vốn hoá",
    "1368": "Phải thu nội bộ khác",
    "138": "Phải thu khác",
    "1381": "Tài sản thiếu chờ xử lý",
    "1383": "Thuế TTĐB của hàng nhập khẩu",
    "1388": "Phải thu khác",
    "141": "Tạm ứng",
    "151": "Hàng mua đang đi đường",
    "152": "Nguyên liệu, vật liệu",
    "153": "Công cụ, dụng cụ",
    "154": "Chi phí sản xuất, kinh doanh dở dang",
    "155": "Sản phẩm",
    "156": "Hàng hóa",
    "157": "Hàng gửi đi bán",
    "158": "Nguyên liệu, vật tư tại kho bảo thuế",
    "171": "Giao dịch mua, bán lại trái phiếu chính phủ",
    "211": "Tài sản cố định hữu hình",
    "212": "Tài sản cố định thuê tài chính",
    "213": "Tài sản cố định vô hình",
    "214": "Hao mòn tài sản cố định",
    "2141": "Hao mòn TSCĐ hữu hình",
    "2142": "Hao mòn TSCĐ thuê tài chính",
    "2143": "Hao mòn TSCĐ vô hình",
    "2147": "Hao mòn BĐSĐT",
    "215": "Tài sản sinh học",
    "2151": "Súc vật nuôi cho sản phẩm định kỳ",
    "21511": "Súc vật nuôi cho sản phẩm định kỳ chưa đạt đến giai đoạn trưởng thành",
    "21512": "Súc vật nuôi cho sản phẩm định kỳ đạt đến giai đoạn trưởng thành",
    "215121": "Nguyên giá",
    "215122": "Giá trị khấu hao lũy kế",
    "2152": "Súc vật nuôi lấy sản phẩm một lần",
    "2153": "Cây trồng theo mùa vụ hoặc lấy sản phẩm một lần",
    "217": "Bất động sản đầu tư",
    "221": "Đầu tư vào công ty con",
    "222": "Đầu tư vào công ty liên doanh, liên kết",
    "228": "Đầu tư khác",
    "2281": "Đầu tư góp vốn vào đơn vị khác",
    "2288": "Đầu tư khác",
    "229": "Dự phòng tổn thất tài sản",
    "2291": "Dự phòng giảm giá chứng khoán kinh doanh",
    "2292": "Dự phòng tổn thất đầu tư vào đơn vị khác",
    "2293": "Dự phòng phải thu khó đòi",
    "2294": "Dự phòng giảm giá hàng tồn kho",
    "2295": "Dự phòng tổn thất tài sản sinh học",
    "241": "Xây dựng cơ bản dở dang",
    "2411": "Mua sắm TSCĐ",
    "2412": "Xây dựng cơ bản",
    "2413": "Sửa chữa, bảo dưỡng định kỳ TSCĐ",
    "2414": "Nâng cấp, cải tạo TSCĐ",
    "242": "Chi phí chờ phân bổ",
    "243": "Tài sản thuế thu nhập hoãn lại",
    "244": "Ký quỹ, ký cược",
    "331": "Phải trả cho người bán",
    "332": "Phải trả cổ tức, lợi nhuận",
    "333": "Thuế và các khoản phải nộp Nhà nước",
    "3331": "Thuế giá trị gia tăng phải nộp",
    "33311": "Thuế GTGT đầu ra",
    "33312": "Thuế GTGT hàng nhập khẩu",
    "3332": "Thuế tiêu thụ đặc biệt",
    "3333": "Thuế xuất, nhập khẩu",
    "3334": "Thuế thu nhập doanh nghiệp",
    "3335": "Thuế thu nhập cá nhân",
    "3336": "Thuế tài nguyên",
    "3337": "Thuế nhà đất, tiền thuê đất",
    "3338": "Thuế bảo vệ môi trường và các loại thuế khác",
    "33381": "Thuế bảo vệ môi trường",
    "33382": "Các loại thuế khác",
    "3339": "Phí, lệ phí và các khoản phải nộp khác",
    "334": "Phải trả người lao động",
    "335": "Chi phí phải trả",
    "336": "Phải trả nội bộ",
    "3361": "Phải trả nội bộ về vốn kinh doanh",
    "3362": "Phải trả nội bộ về chênh lệch tỷ giá",
    "3363": "Phải trả nội bộ về chi phí đi vay đủ điều kiện được vốn hóa",
    "3368": "Phải trả nội bộ khác",
    "337": "Thanh toán theo tiến độ hợp đồng xây dựng",
    "338": "Phải trả, phải nộp khác",
    "3381": "Tài sản thừa chờ giải quyết",
    "3382": "Kinh phí công đoàn",
    "3383": "Bảo hiểm xã hội",
    "3384": "Bảo hiểm y tế",
    "3386": "Bảo hiểm thất nghiệp",
    "3387": "Doanh thu chờ phân bổ",
    "3388": "Phải trả, phải nộp khác",
    "341": "Vay và nợ thuê tài chính",
    "3411": "Các khoản đi vay",
    "3412": "Nợ thuê tài chính",
    "343": "Trái phiếu phát hành",
    "3431": "Trái phiếu thường",
    "3432": "Trái phiếu chuyển đổi",
    "344": "Nhận ký quỹ, ký cược",
    "347": "Thuế thu nhập hoãn lại phải trả",
    "352": "Dự phòng phải trả",
    "3521": "Dự phòng bảo hành sản phẩm, hàng hóa",
    "3522": "Dự phòng bảo hành công trình xây dựng",
    "3523": "Dự phòng tái cơ cấu doanh nghiệp",
    "3525": "Dự phòng phải trả khác",
    "353": "Quỹ khen thưởng, phúc lợi",
    "3531": "Quỹ khen thưởng",
    "3532": "Quỹ phúc lợi",
    "3533": "Quỹ phúc lợi đã hình thành TSCĐ",
    "3534": "Quỹ thưởng ban quản lý điều hành công ty",
    "356": "Quỹ phát triển khoa học và công nghệ",
    "3561": "Quỹ phát triển khoa học và công nghệ",
    "3562": "Quỹ phát triển khoa học và công nghệ đã hình thành tài sản",
    "357": "Quỹ bình ổn giá",
    "411": "Vốn đầu tư của chủ sở hữu",
    "4111": "Vốn góp của chủ sở hữu",
    "41111": "Cổ phiếu phổ thông có quyền biểu quyết",
    "41112": "Cổ phiếu ưu đãi",
    "4112": "Thặng dư vốn",
    "4113": "Quyền chọn chuyển đổi trái phiếu",
    "4118": "Vốn khác",
    "412": "Chênh lệch đánh giá lại tài sản",
    "413": "Chênh lệch tỷ giá hối đoái",
    "414": "Quỹ đầu tư phát triển",
    "418": "Các quỹ khác thuộc vốn chủ sở hữu",
    "419": "Cổ phiếu mua lại của chính mình",
    "421": "Lợi nhuận sau thuế chưa phân phối",
    "4211": "Lợi nhuận sau thuế chưa phân phối lũy kế đến cuối năm trước",
    "4212": "Lợi nhuận sau thuế chưa phân phối năm nay",
    "511": "Doanh thu bán hàng và cung cấp dịch vụ",
    "515": "Doanh thu hoạt động tài chính",
    "521": "Các khoản giảm trừ doanh thu",
    "621": "Chi phí nguyên liệu, vật liệu trực tiếp",
    "622": "Chi phí nhân công trực tiếp",
    "623": "Chi phí sử dụng máy thi công",
    "6231": "Chi phí nhân công",
    "6232": "Chi phí vật liệu",
    "6233": "Chi phí dụng cụ sản xuất",
    "6234": "Chi phí khấu hao máy thi công",
    "6237": "Chi phí dịch vụ mua ngoài",
    "6238": "Chi phí bằng tiền khác",
    "627": "Chi phí sản xuất chung",
    "6271": "Chi phí nhân viên phân xưởng",
    "6272": "Chi phí vật liệu",
    "6273": "Chi phí dụng cụ sản xuất",
    "6274": "Chi phí khấu hao TSCĐ",
    "6275": "Thuế, phí, lệ phí",
    "6277": "Chi phí dịch vụ mua ngoài",
    "6278": "Chi phí bằng tiền khác",
    "632": "Giá vốn hàng bán",
    "635": "Chi phí tài chính",
    "641": "Chi phí bán hàng",
    "6411": "Chi phí nhân viên",
    "6412": "Chi phí vật liệu, bao bì",
    "6413": "Chi phí dụng cụ, đồ dùng",
    "6414": "Chi phí khấu hao TSCĐ",
    "6415": "Thuế, phí, lệ phí",
    "6417": "Chi phí dịch vụ mua ngoài",
    "6418": "Chi phí bằng tiền khác",
    "642": "Chi phí quản lý doanh nghiệp",
    "6421": "Chi phí nhân viên quản lý",
    "6422": "Chi phí vật liệu quản lý",
    "6423": "Chi phí đồ dùng văn phòng",
    "6424": "Chi phí khấu hao TSCĐ",
    "6425": "Thuế, phí và lệ phí",
    "6426": "Chi phí dự phòng",
    "6427": "Chi phí dịch vụ mua ngoài",
    "6428": "Chi phí bằng tiền khác",
    "711": "Thu nhập khác",
    "811": "Chi phí khác",
    "821": "Chi phí thuế thu nhập doanh nghiệp",
    "8211": "Chi phí thuế TNDN hiện hành",
    "82111": "Chi phí thuế thu nhập doanh nghiệp hiện hành theo quy định của Luật thuế thu nhập doanh nghiệp",
    "82112": "Chi phí thuế thu nhập doanh nghiệp bổ sung theo quy định về thuế tối thiểu toàn cầu",
    "8212": "Chi phí thuế TNDN hoãn lại",
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
        if user_query in acc_name.lower() or user_query in acc_num:
            results.append(f"• TK {acc_num}: {acc_name}")
            
    if results:
        bot_reply = "Kết quả tìm kiếm:\\n" + "\\n".join(results)
    else:
        bot_reply = "Không tìm thấy tài khoản nào khớp với dữ liệu bạn nhập."
        
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

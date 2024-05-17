import pickle
import socket
from _thread import *
from game import Game


server = "127.0.0.1"
port = 3456

# tạo một socket sử dụng IPv4 và giao thức TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set() # Lưu trữ các kết nối đang hoạt động
games = {} # Từ điển rỗng để lưu trữ các game
idCount = 0 # Biến toàn cục dùng để đếm số lượng các kết nối

# Hàm xử lý kết nối tới Client
# conn: đối tượng kết nối
# p: là người chơi, 0 hoặc 1
#gameId: là ID của game
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p))) # Gửi thông tin về người chơi tới Client

    reply = ""
    # Vòng lặp xử lí dữ liệu từ Client
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game ",gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))

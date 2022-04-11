import http.server
import socketserver

SERVER_PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True # -- El socket esta creada pero tengo que indicar que lo quiero reutilizar si se me queda pillao

# -- Use the http.server Handler
handler = http.server.SimpleHTTPRequestHandler # -- cuando le diga a mi socket que se ponga a escuchar todas las peticiones, ya tengo un manejador que entiende http y sabe que hacer cuando recibe un get, post...

# -- Open the socket server
with socketserver.TCPServer(("", SERVER_PORT), handler) as httpd: # -- La d es de demonio, tb puedes llamarle web_server / En "" va la IP localhost automáticamente / Se une ip y port como si fuera un bind

    print("Serving at PORT", SERVER_PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server Stopped!")
        httpd.server_close()
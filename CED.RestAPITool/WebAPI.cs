using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace CED.RestAPITool
{
    public class WebAPI
    {
        private HttpListener _listener;
        private Thread listenerThread;

        public WebAPI()
        {
            _listener = new HttpListener();
            _listener.Prefixes.Add("http://localhost:51765/api/test");

            listenerThread = new Thread(() =>
            {
                while (_listener.IsListening)
                {
                    try
                    {
                        var context = _listener.GetContext();
                        var response = context.Response;
                        string responseString = "{\"message\": \"Hello from WinForms API!\"}";
                        byte[] buffer = Encoding.UTF8.GetBytes(responseString);
                        response.ContentType = "application/json";
                        response.ContentLength64 = buffer.Length;
                        response.OutputStream.Write(buffer, 0, buffer.Length);
                        response.OutputStream.Flush();
                        response.OutputStream.Close();
                    }
                    catch (HttpListenerException) { break; }
                }
            });
            listenerThread.Start();
        }
    }
}

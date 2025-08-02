using System.Net;

namespace CED.RestAPITool.Interfaces
{
    public interface IActionResult
    {
        void ExecuteResult(HttpListenerContext context);
    }
}

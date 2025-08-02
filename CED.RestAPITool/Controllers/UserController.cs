using CED.RestAPITool.Interfaces;

namespace CED.RestAPITool.Controllers
{
    public class UserController : BaseController
    {
        public IActionResult GetUser()
        {
            return JsonResult(new
            {
                Id = 1,
                Name = "Phuong Nguyen",
            });
        }

        public IActionResult CheckInfor(int id, string name)
        {
            return JsonResult(new
            {
                Id = 1,
                Name = "Phuong Nguyen 2",
            });
        }
    }
}

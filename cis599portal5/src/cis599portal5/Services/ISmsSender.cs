using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace cis599portal5.Services
{
    public interface ISmsSender
    {
        Task SendSmsAsync(string number, string message);
    }
}

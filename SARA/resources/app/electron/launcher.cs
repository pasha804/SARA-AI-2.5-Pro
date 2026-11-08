using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

[assembly: AssemblyTitle("SARA AI 3.0 Enterprise Pro")]
[assembly: AssemblyDescription("SARA AI 3.0 Enterprise Pro Desktop Companion Launcher")]
[assembly: AssemblyProduct("SARA AI 3.0 Enterprise Pro")]
[assembly: AssemblyCompany("Pasha Dev (pasha804)")]
[assembly: AssemblyCopyright("Copyright © 2026 Muhammad Mubashar (pasha804). All rights reserved.")]
[assembly: AssemblyVersion("3.0.0.0")]
[assembly: AssemblyFileVersion("3.0.0.0")]

internal static class Program
{
    [STAThread]
    private static int Main(string[] args)
    {
        string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
        string runtimePath = Path.Combine(baseDirectory, "SARA-runtime.exe");
        if (!File.Exists(runtimePath))
        {
            runtimePath = Path.Combine(baseDirectory, "MYRAA-runtime.exe");
        }

        if (!File.Exists(runtimePath))
        {
            MessageBox.Show(
                "SARA-runtime.exe was not found in " + baseDirectory + ".\nPlease reinstall SARA AI 3.0 Enterprise Pro.",
                "SARA AI 3.0 Launch Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return 1;
        }

        try
        {
            Environment.SetEnvironmentVariable("NODE_OPTIONS", null, EnvironmentVariableTarget.Process);
            Environment.SetEnvironmentVariable("ELECTRON_RUN_AS_NODE", null, EnvironmentVariableTarget.Process);

            var startInfo = new ProcessStartInfo
            {
                FileName = runtimePath,
                Arguments = JoinArguments(args),
                WorkingDirectory = baseDirectory,
                UseShellExecute = false,
            };
            Process runtime = Process.Start(startInfo);
            if (runtime == null) return 1;

            runtime.WaitForExit();
            return runtime.ExitCode;
        }
        catch (Exception error)
        {
            MessageBox.Show(
                "SARA AI 3.0 could not be launched.\r\n\r\n" + error.Message,
                "SARA AI 3.0 Failed to Start",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return 1;
        }
    }

    private static string JoinArguments(string[] args)
    {
        if (args == null || args.Length == 0) return string.Empty;
        var quoted = new string[args.Length];
        for (int index = 0; index < args.Length; index++)
        {
            string value = args[index] ?? string.Empty;
            quoted[index] = "\"" + value.Replace("\\", "\\\\").Replace("\"", "\\\"") + "\"";
        }
        return string.Join(" ", quoted);
    }
}

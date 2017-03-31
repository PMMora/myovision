using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DHFMover
{
    public partial class Form1 : Form
    {
        FolderBrowserDialog srcfbd = new FolderBrowserDialog();
        FolderBrowserDialog destfbd = new FolderBrowserDialog();

        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            srcfbd.Description = "Select Source Folder";
            if (srcfbd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                MessageBox.Show(srcfbd.SelectedPath);
                Script.srcPath = srcfbd.SelectedPath;
                textBox1.Text = Script.srcPath;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            destfbd.Description = "Select Destination Folder";
            if (destfbd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                MessageBox.Show(destfbd.SelectedPath);
                textBox2.Text = destfbd.SelectedPath;
                Script.destPath = destfbd.SelectedPath;
        }

        private void button3_Click(object sender, EventArgs e)
        {
            Script.PythonScript();
            MessageBox.Show("Files moved from " + Script.srcPath + " to " + Script.destPath);
        }
    }
    public class Script
    {
        public static string srcPath = "";
        public static string destPath = "";
        public static void PythonScript()
        {
            string pythonExe = @"C:\Python34\python.exe";
            string fileScript = @""+System.AppDomain.CurrentDomain.BaseDirectory + "\\MovingFiles.py";
            Console.Write(fileScript);
            Process moveFiles = new Process();
            moveFiles.StartInfo.FileName = pythonExe;
            moveFiles.StartInfo.Arguments = fileScript + " " + srcPath + " " + destPath;
            moveFiles.StartInfo.UseShellExecute = false;
            moveFiles.StartInfo.RedirectStandardOutput = true;
            moveFiles.StartInfo.RedirectStandardError = true;
            moveFiles.Start();

            StreamReader myStreamReader = moveFiles.StandardError;
            string myString = myStreamReader.ReadToEnd();

            moveFiles.WaitForExit();
            moveFiles.Close();

            Console.WriteLine("Value received from script: " + myString);



        }
    }
}

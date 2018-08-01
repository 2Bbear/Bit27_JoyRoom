using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

using System.Windows.Forms;
using System.Net.Sockets;
using System.Net;
using System.IO;

namespace WPF_HowToUseMjpeg_0725
{
    /// <summary>
    /// HistoryVideo.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class HistoryVideo : Window
    {
       
        string mypath = "save\\";

        public HistoryVideo()
        {
            Console.WriteLine(mypath);
            InitializeComponent();
        }

        #region 비디오 플레이어

        //시작
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            MediaElement1.Play();
        }
        //멈춤
        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            MediaElement1.Stop();
        }
        //일시정지
        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            MediaElement1.Pause();
        }

        //파일 열기
        private void Button_Click_3(object sender, RoutedEventArgs e)
        {
            OpenFileDialog ofd;
            ofd = new OpenFileDialog();
            ofd.AddExtension = true;
            ofd.DefaultExt = "*.*";
            ofd.Filter = "Media Files (*.*)|*.*";
            ofd.ShowDialog();

            try
            {
                MediaElement1.Source = new Uri(ofd.FileName);
            }
            catch
            {
                new NullReferenceException("Error");

            }

            System.Windows.Threading.DispatcherTimer dispatcherTimer = new System.Windows.Threading.DispatcherTimer();
            dispatcherTimer.Tick += new EventHandler(timer_Tick);
            dispatcherTimer.Interval = new TimeSpan(0, 0, 1);
            dispatcherTimer.Start();
        }

        void timer_Tick(object sender, EventArgs e)
        {
            Slider1.Value = MediaElement1.Position.TotalSeconds;

        }

        //재생슬라이더바
        private void Slider1_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            TimeSpan ts = TimeSpan.FromSeconds(e.NewValue);
            MediaElement1.Position = ts;
        }

        //볼륨
        private void Slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            MediaElement1.Volume = Slider2.Value;
        }

        private void MediaElement1_MediaOpened(object sender, RoutedEventArgs e)
        {
            if (MediaElement1.NaturalDuration.HasTimeSpan)
            {
                TimeSpan ts = TimeSpan.FromMilliseconds(MediaElement1.NaturalDuration.TimeSpan.TotalMilliseconds);
                Slider1.Maximum = ts.TotalSeconds;
            }
        }
        #endregion

        #region 파일 가져오기
        //TcpClient myclient;

        public void Connect()
        {

            string message = "@" + comboBox1.Text + comboBox2.Text + comboBox3.Text + comboBox4.Text + comboBox5.Text + "_cam" + comboBox6.Text + ".avi";

            if (message.Equals(""))
            {
                return;
            }

            try
            {
                Int32 port = 9009;
                TcpClient client = new TcpClient("192.168.0.21", port);

                // Translate the passed message into ASCII and store it as a Byte array.
                Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);
                //Console.Write(data);
                // Get a client stream for reading and writing.
                //  Stream stream = client.GetStream();

                NetworkStream stream = client.GetStream();

                // Send the message to the connected TcpServer. 
                stream.Write(data, 0, data.Length);

                Console.WriteLine("Sent: {0}", message);


                // Receive the TcpServer.response.

                // Buffer to store the response bytes.
                data = new Byte[1024];

                // String to store the response ASCII representation.
                String responseData = String.Empty;

                string path = mypath + comboBox1.Text + comboBox2.Text + comboBox3.Text + comboBox4.Text + comboBox5.Text + "_cam" + comboBox6.Text + ".avi";

                //폴더 없으면 폴더 만드는 코드
                string sDirPath;
                sDirPath =mypath;
                DirectoryInfo di = new DirectoryInfo(sDirPath);
                if (di.Exists == false)
                {
                    di.Create();
                }
                
                using (FileStream fs = File.Create(path))
                {
                    while (true)
                    {
                        // Read the first batch of the TcpServer response bytes.
                        Int32 bytes = stream.Read(data, 0, data.Length);

                        responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                        Console.WriteLine("Received: {0}", responseData);

                        Byte[] info = new UTF8Encoding(true).GetBytes(responseData);

                        // Add some information to the file.
                        //fs.Write(info, 0, info.Length);
                        fs.Write(data, 0, data.Length);
                        if (responseData.Equals(""))
                        {
                            break;
                        }
                    }
                }


                // Close everything.
                stream.Close();
                client.Close();
            }
            catch (ArgumentNullException e)
            {
                Console.WriteLine("ArgumentNullException: {0}", e);
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }

            Console.WriteLine("\n Press Enter to continue...");

        }

        private void Button_Click_4(object sender, RoutedEventArgs e)
        {
            Connect();

        }
        #endregion
    }
}

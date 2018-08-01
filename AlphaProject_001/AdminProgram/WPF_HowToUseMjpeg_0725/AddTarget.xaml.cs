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

using System.Net.Sockets;
using System.Net;
using System.IO;
using System.Windows.Forms;


namespace WPF_HowToUseMjpeg_0725
{
    /// <summary>
    /// addtarget.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class addtarget : Window
    {
        string serverip = "220.90.196.196";
        int serverport = 9009;
        public addtarget()
        {
            InitializeComponent();
        }

        #region Event Method
        //찾아보기 버튼 클릭
        private void btn_find_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog photo;
            photo = new OpenFileDialog();
            photo.AddExtension = true;
            photo.DefaultExt = "*.*";
            photo.Filter = "Picture Files (*.*)|*.*";
            photo.ShowDialog();

            try
            {
                //이미지 경로 받아오기
                textbox_filename.Text = photo.FileName;
                //해당 경로의 사진 띄우기
                PrintImageOnImageControl();
            }
            catch
            {
                new NullReferenceException("Error");
            }
        }
        //보내는 버튼 클릭
        private void btn_send_Click(object sender, RoutedEventArgs e)
        {
            TcpClient tcpClient = new TcpClient();
            tcpClient.Connect(serverip, Convert.ToInt32(serverport));
            NetworkStream networkStream = tcpClient.GetStream();


            FileInfo file = new FileInfo(textbox_filename.Text);
            FileStream fs = file.OpenRead();

            try
            {
                if (networkStream.CanWrite && networkStream.CanRead)
                {

                    string[] filenames = textbox_filename.Text.Split('\\');
                    string filename = filenames[filenames.Length - 1];

                    Byte[] sendBytes = Encoding.ASCII.GetBytes(filename);
                    networkStream.Write(sendBytes, 0, sendBytes.Length);


                    byte[] FileBytes;
                    FileBytes = new byte[fs.Length];
                    fs.Read(FileBytes, 0, FileBytes.Length);
                    networkStream.Write(FileBytes, 0, FileBytes.Length);
                    Console.WriteLine("보내기 성공");
                }
            }
            catch (SocketException)
            {
                Console.WriteLine("서버접속에 실패하였습니다.");
                
            }
            catch (System.IO.IOException)
            {
                Console.WriteLine("서버접속에 실패하였습니다.");
               
            }
            catch (Exception ex)
            {
                Console.WriteLine("서버접속에 실패하였습니다.");
                System.Windows.Forms.MessageBox.Show(ex.ToString());
            }
            finally
            {
                fs.Flush();
                fs.Close();

                networkStream.Flush();
                networkStream.Close();

                tcpClient.Close();
            }
        }
        #endregion

        #region Custom Method
        //사진을 image컨트롤에 띄우는 함수
        private void PrintImageOnImageControl()
        {
            //비트맵이미지 만들어서 이미지 넣기
            BitmapImage b = new BitmapImage();
            b.BeginInit();
            b.UriSource = new Uri(textbox_filename.Text);
            b.EndInit();
            image_view.Source = b;
            //var image = sender as Image;
            //image.Source = b;
        }
        #endregion

    }
}

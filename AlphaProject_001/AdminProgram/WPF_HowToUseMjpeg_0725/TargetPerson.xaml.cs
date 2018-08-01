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
    /// TargetPerson.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class TargetPerson : Window
    {
        public TargetPerson()
        {
            InitializeComponent();
        }


        private void Button_Click(object sender, RoutedEventArgs e)
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
                label1.Text = photo.FileName;
            }
            catch
            {
                new NullReferenceException("Error");
            }

          
        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            TcpClient tcpClient = new TcpClient();
            tcpClient.Connect("220.90.196.196", Convert.ToInt32(9009));
            NetworkStream networkStream = tcpClient.GetStream();


            FileInfo file = new FileInfo(label1.Text);
            FileStream fs = file.OpenRead();

            try
            {
                if (networkStream.CanWrite && networkStream.CanRead)
                {
              
                    string[] filenames = label1.Text.Split('\\');
                    string filename = filenames[filenames.Length - 1];

                    Byte[] sendBytes = Encoding.ASCII.GetBytes(filename);
                    networkStream.Write(sendBytes, 0, sendBytes.Length);

               
                    byte[] FileBytes;
                    FileBytes = new byte[fs.Length];
                    fs.Read(FileBytes, 0, FileBytes.Length);
                    networkStream.Write(FileBytes, 0, FileBytes.Length);
                }
            }
            catch (SocketException)
            {
                System.Windows.Forms.MessageBox.Show("서버접속에 실패하였습니다.");
            }
            catch (System.IO.IOException)
            {
                System.Windows.Forms.MessageBox.Show("서버접속에 실패하였습니다.");
            }
            catch (Exception ex)
            {
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

        private void image_Loaded(object sender, RoutedEventArgs e)
        {
            //비트맵이미지 만들어서 이미지 넣기
            BitmapImage b = new BitmapImage();
            b.BeginInit();
            b.UriSource = new Uri(label1.Text);
            b.EndInit();
            var image = sender as Image;
            image.Source = b;
        }
    }
}

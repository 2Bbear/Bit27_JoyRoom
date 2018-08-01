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
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Drawing;

using AForge;
using MjpegProcessor;
using MySql.Data.MySqlClient;
using System.Data.Odbc;

namespace WPF_HowToUseMjpeg_0725
{
    //detail_show_iamge에 출력할 Cam 선택을 위한 플래그
    public enum BigCameraFlag
    {
        Base=0,
        Cam_1 = 1,
        Cam_2 = 2,
        Cam_3 = 3,
        Cam_4 = 4

    }
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {
        #region Member Field
        //DB 객체
        MySqlConnection dbconn;
        

        List<string> cam_ip = new List<string>();


        //image 컨트롤에 매 프레임 출력해줄 이벤트 객체
        public MjpegDecoder _mjpeg1;
        public MjpegDecoder _mjpeg2;
        public MjpegDecoder _mjpeg3;
        public MjpegDecoder _mjpeg4;

        public BigCameraFlag mybigvideoflag = new BigCameraFlag();
        #endregion

        //생성자
        public MainWindow()
        {
            InitializeComponent();
            //DB 연결
            ConnectDB("192.168.0.21");
            //캠 아이피 가져오기
            GetCamIPData();

            
            //1번 카메라
            _mjpeg1 = new MjpegDecoder();
            _mjpeg1.FrameReady += mjpeg_FrameReady1;
            //2번 카메라
            _mjpeg2 = new MjpegDecoder();
            _mjpeg2.FrameReady += mjpeg_FrameReady2;
            //3번 카메라
            _mjpeg3 = new MjpegDecoder();
            _mjpeg3.FrameReady += mjpeg_FrameReady3;
            //4번 카메라
            _mjpeg4 = new MjpegDecoder();
            _mjpeg4.FrameReady += mjpeg_FrameReady4;
            Console.WriteLine("시작");
        }

        //파괴자
        ~MainWindow()
        {
            //DB 연결 해제
            DisConnectDB();
        }
  
        #region Event Method
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _mjpeg1.ParseStream(new Uri("http://" + cam_ip[0] + ":5000/video_feed"));
            }
            catch (Exception)
            {
                Console.WriteLine("1번캠 uri 없음");
            }

            try
            {
                _mjpeg2.ParseStream(new Uri("http://" + cam_ip[1] + ":5000/video_feed"));
            }
            catch (Exception)
            {
                Console.WriteLine("2번캠 uri 없음");
            }

            try
            {
                _mjpeg3.ParseStream(new Uri("http://" + cam_ip[2] + ":5000/video_feed"));
            }
            catch (Exception)
            {
                Console.WriteLine("3번캠 uri 없음");
            }

            try
            {
                _mjpeg4.ParseStream(new Uri("http://" + cam_ip[3] + ":5000/video_feed"));
            }
            catch (Exception)
            {
                Console.WriteLine("4번캠 uri 없음");
            }




        }

        //Menu Item Event
        private void add_target_Click(object sender, RoutedEventArgs e)
        {
            addtarget settingWindow1 = new addtarget();
            settingWindow1.Show();
        }

        private void h_log_Click(object sender, RoutedEventArgs e)
        {
            HistoryLog settingWindow2 = new HistoryLog(dbconn);
            settingWindow2.Show();
        }

        private void h_video_Click(object sender, RoutedEventArgs e)
        {
            HistoryVideo settingWindow3 = new HistoryVideo();
            settingWindow3.Show();
        }

        private void MenuItem_Click(object sender, RoutedEventArgs e)
        {
            Credit settingWindow4 = new Credit();
            settingWindow4.ShowDialog();
        }
        //Cam Image ControllerEvent
        //1번 카메라 디코더 프레임 이벤트 연결
        private void mjpeg_FrameReady1(object sender, FrameReadyEventArgs e)
        {
            image_1.Source = e.BitmapImage;

            //큰 화면을 위한 플래그
            if (mybigvideoflag == BigCameraFlag.Cam_1)
            {
                detail_show_iamge.Source = image_1.Source;
            }
        }
        private void image_1_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            mybigvideoflag = BigCameraFlag.Cam_1;
        }

        //2번 카메라 디코더 프레임 이벤트 연결
        private void mjpeg_FrameReady2(object sender, FrameReadyEventArgs e)
        {
            image_2.Source = e.BitmapImage;

            //큰 화면을 위한 플래그
            if (mybigvideoflag == BigCameraFlag.Cam_2)
            {
                detail_show_iamge.Source = image_2.Source;
            }
        }
        private void image_2_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            mybigvideoflag = BigCameraFlag.Cam_2;
        }

        //3번 카메라 디코더 프레임 이벤트 연결
        private void mjpeg_FrameReady3(object sender, FrameReadyEventArgs e)
        {
            image_3.Source = e.BitmapImage;

            //큰 화면을 위한 플래그
            if (mybigvideoflag == BigCameraFlag.Cam_3)
            {
                detail_show_iamge.Source = image_3.Source;
            }
        }
        private void image_3_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            mybigvideoflag = BigCameraFlag.Cam_3;
        }

        //4번 카메라 디코더 프레임 이벤트 연결
        private void mjpeg_FrameReady4(object sender, FrameReadyEventArgs e)
        {
            image_4.Source = e.BitmapImage;

            //큰 화면을 위한 플래그
            if (mybigvideoflag == BigCameraFlag.Cam_4)
            {
                detail_show_iamge.Source = image_4.Source;
            }
        }
        private void image_4_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            mybigvideoflag = BigCameraFlag.Cam_4;
        }
        #endregion


        #region Custom Method
        //Custom Method
        //DB연결하는 메소드
        private void ConnectDB(string _server = "220.90.196.196", string _userid = "bit27", string _password = "123123", string _database = "sys", uint _port = 3306)
        {
            //DB 연결
            try
            {
                MySqlConnectionStringBuilder builder = new MySqlConnectionStringBuilder();
                builder.Server = _server;
                builder.UserID = _userid;
                builder.Password = _password;
                builder.Database = _database;
                builder.Port = _port;

                dbconn = new MySqlConnection(builder.ToString());
                dbconn.Open();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                throw;
            }
        }
        //DB 연결 해제 메소드
        private void DisConnectDB()
        {
            dbconn.Close();
        }
        //Selete IP가져오기
        private void GetCamIPData()
        {
            //가지고 있던 캠 ip 전부 없애기
            cam_ip.Clear();
            //
            
            string sql = "SELECT * FROM sys.ip;";

            //ExecuteReader를 이용하여
            //연결 모드로 데이타 가져오기
            MySqlCommand cmd = new MySqlCommand(sql, dbconn);
            MySqlDataReader rdr = cmd.ExecuteReader();
            while (rdr.Read())
            {
                cam_ip.Add(rdr["ip"].ToString());
            }
            rdr.Close();
            
        }
        #endregion



    }
}

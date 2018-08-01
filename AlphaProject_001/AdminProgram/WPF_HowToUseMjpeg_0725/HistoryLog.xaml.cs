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

using MySql.Data.MySqlClient;
using System.Data.Odbc;

namespace WPF_HowToUseMjpeg_0725
{
    struct Log
    {
        public string flilename;
        public int time;
        public string name;
        public string coordinates;
        public string clothescolor;

        public Log(string flilename, int time, string name, string coordinates, string clothescolor)
        {
            this.flilename = flilename;
            this.time = time;
            this.name = name;
            this.coordinates = coordinates;
            this.clothescolor = clothescolor;
        }
    }
    /// <summary>
    /// HistoryLog.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class HistoryLog : Window
    {
        

        #region Member Field

        MySqlConnection myconn;
        #endregion


        public HistoryLog(MySqlConnection _myconn)
        {
            InitializeComponent();

            
            //Controll Initializing
            combobox_camnum.SelectedIndex = 0;
            combobox_day.SelectedIndex = 0;
            combobox_hour.SelectedIndex = 0;
            combobox_minute.SelectedIndex = 0;
            combobox_month.SelectedIndex = 0;
            combobox_year.SelectedIndex = 0;
            combobox_second.SelectedIndex = 0;

            listview_loglist.Items.Clear();

            //member field Initializing
            myconn = _myconn;
        }
        #region Cusotm Method
        //Custom Methode
        //Select 문 db에서 로그 가져와서 리스트로 출력
        private List<Log> GetLog(string _year, string _month, string _day, string _hour, string _minute, string _secound, string _camnum)
        {
            List<Log> result = new List<Log>();
            
            string sql = "SELECT * FROM sys."+ _camnum+"logtable " + "WHERE filename="+_year+_month+_day+_hour+_minute+";";

            //ExecuteReader를 이용하여
            //연결 모드로 데이타 가져오기
            MySqlCommand cmd = new MySqlCommand(sql, myconn);
            MySqlDataReader rdr = cmd.ExecuteReader();
            while (rdr.Read())
            {
                result.Add(new Log(rdr["filename"].ToString(),int.Parse(rdr["time"].ToString()),rdr["name"].ToString(),rdr["coordinates"].ToString(),rdr["clothescolor"].ToString()));
            }
            rdr.Close();


            return result;
        }

        public class LogListViewTemplet
        {
            public string Filename { get; set; }
            public int Time { get; set; }
            public string Name { get; set; }
            public string Coordinates { get; set; }
            public string Clothes { get; set; }
        }
        private void PrintLoglistview(List<Log> result)
        {
            List<LogListViewTemplet> itemtemp = new List<LogListViewTemplet>();

            foreach (Log item in result)
            {
                itemtemp.Add(new LogListViewTemplet() { Filename =item.flilename, Time=item.time, Name=item.name, Coordinates=item.coordinates, Clothes=item.clothescolor});
            }
            listview_loglist.Items.Refresh();
            listview_loglist.ItemsSource = itemtemp;
        }

        #endregion

        #region Event Method
        //조회버튼 클릭
        private void checkbtn_Click(object sender, RoutedEventArgs e)
        {
            //컨트롤에 값 형변환
            //년
            ComboBoxItem _y = combobox_year.SelectedItem as ComboBoxItem;
            string year = _y.Content.ToString();
            //월
            ComboBoxItem _m = combobox_month.SelectedItem as ComboBoxItem;
            string month = _m.Content.ToString();
            //날
            ComboBoxItem _d = combobox_day.SelectedItem as ComboBoxItem;
            string day = _d.Content.ToString();
            //시
            ComboBoxItem _h = combobox_hour.SelectedItem as ComboBoxItem;
            string hour = _h.Content.ToString();
            //분
            ComboBoxItem _mi = combobox_minute.SelectedItem as ComboBoxItem;
            string minute = _mi.Content.ToString();
            //초
            ComboBoxItem _s = combobox_second.SelectedItem as ComboBoxItem;
            string second = _s.Content.ToString();
            //캠 번호
            ComboBoxItem _cn = combobox_camnum.SelectedItem as ComboBoxItem;
            string camnum = _cn.Content.ToString();

            List<Log> temp=GetLog(year,
                month, 
                day,
                hour,
                minute,
                second,
                camnum
                );

            PrintLoglistview(temp);

        }
        #endregion

    }
}

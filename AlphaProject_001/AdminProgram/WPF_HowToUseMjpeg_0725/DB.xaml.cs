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

//Using namespaces 
using System.Data;
using MySql.Data.MySqlClient;
using System.Configuration;

namespace WPF_HowToUseMjpeg_0725
{
    /// <summary>
    /// DB.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DB : Window
    {

        #region 디비 접속
        MySqlConnection conn = new
        MySqlConnection(ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString);


        public DB()
        {
            InitializeComponent();
        }
        #endregion

        #region 디비 넣기
        private void btnloaddata_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                conn.Open();
                MySqlCommand cmd = new MySqlCommand("select * from cam1logtable", conn);
                MySqlDataAdapter adp = new MySqlDataAdapter(cmd);
                DataSet ds = new DataSet();
                adp.Fill(ds, "LoadDataBinding");
                dataGridCustomers.DataContext = ds;
            }
            catch (MySqlException ex)
            {
                MessageBox.Show(ex.ToString());
            }
            finally
            {
                conn.Close();
            }
        }
        #endregion

       
    }
}

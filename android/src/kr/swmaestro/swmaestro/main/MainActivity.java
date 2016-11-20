package kr.swmaestro.swmaestro.main;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;

import kr.swmaestro.swmaestro.GcmTestActivity;
import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataUser;
import kr.swmaestro.swmaestro.document.DocumentListTask;
import kr.swmaestro.swmaestro.login.LoginActivity;
import kr.swmaestro.swmaestro.notice.NoticeTask;
import kr.swmaestro.swmaestro.other.BaseAsyncTask;
import kr.swmaestro.swmaestro.other.BaseAsyncTask2;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager.NameNotFoundException;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.gcm.GoogleCloudMessaging;

public class MainActivity extends ActionBarActivity implements OnClickListener {
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;
	private DataUser mDataUser;

	private TextView tvProfileID, tvProfileName, tvProfileAge, tvProfileCourseTerm, tvProfileCourseStep;
	private Button btnNotice, btnDocument1, btnDocument2;
	private ImageButton iBtnLogout;

	/** GCM **/
	public static final String EXTRA_MESSAGE = "message";
	public static final String PROPERTY_REG_ID = "registration_id";
	private static final String PROPERTY_APP_VERSION = "appVersion";
	private final static int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
	String SENDER_ID = "6181800579";
	GoogleCloudMessaging gcm;
	SharedPreferences prefs;
	String regid;

	private TextView tvTest;
	private Button btnGcmTest;
	
	/** GPS **/
	Geocoder gc;
    WifiManager wifi;
    public static List<ScanResult> scanResultList;
    public static int scanResultSize;
    public static String locationString;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.main);
		mContext = this;

		setVariable();
		setProfile();

		// Check device for Play Services APK.
		if (checkPlayServices()) {
			gcm = GoogleCloudMessaging.getInstance(this);
			regid = getRegistrationId(mContext);

			if (regid.isEmpty()) {
				Log.d(TAG, "regid is Empty");
				registerInBackground();
			} else{
				new RegistrationTask(mContext, "등록", regid).execute();
			}
		} else {
			Log.i(TAG, "No valid Google Play Services APK found.");
		}

		// Emulator
		//		Log.d(TAG, "Build.Model : " + Build.MODEL);
		//		Log.d(TAG, "--Build-- " + 
		//					"\nBOARD : " + Build.BOARD +
		//					"\nBOOTLOADER : " + Build.BOOTLOADER +
		//					"\nBRAND : " + Build.BRAND +
		//					"\nCPU_ABI : " + Build.CPU_ABI +
		//					"\nCPU_ABI2 : " + Build.CPU_ABI2 +
		//					"\nDEVICE : " + Build.DEVICE +
		//					"\nDISPLAY : " + Build.DISPLAY +
		//					"\nFINGERPRINT : " + Build.FINGERPRINT +
		//					"\nHARDWARE : " + Build.HARDWARE +
		//					"\nHOST : " + Build.HOST +
		//					"\nID : " + Build.ID +
		//					"\nMANUFACTURER : " + Build.MANUFACTURER +
		//					"\nMODEL : " + Build.MODEL +
		//					"\nPRODUCT : " + Build.PRODUCT +
		//					"\nSERIAL : " + Build.SERIAL +
		//					"\nTAGS : " + Build.TAGS +
		//					"\nTIME : " + Build.TIME +
		//					"\nTYPE : " + Build.TYPE +
		//					"\nUNKNOWN : " + Build.UNKNOWN +
		//					"\nUSER : " + Build.USER
		//				);


		/** GPS **/
		// Geocoder
		gc = new Geocoder(this, Locale.KOREAN);

		// LocationManager
		LocationManager locationManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
		LocationListener locationListner = new LocationListener() {
			@Override
			public void onStatusChanged(String provider, int status, Bundle extras) {
				
			}
			@Override
			public void onProviderEnabled(String provider) {

			}
			@Override
			public void onProviderDisabled(String provider) {

			}			
			@Override
			public void onLocationChanged(Location location) {
//				Log.d(TAG, "Location : " + location.toString());
				double lat = location.getLatitude();
				double lon = location.getLongitude();
				String addressString = "";
				try {

					List<Address> addresses = gc.getFromLocation(lat, lon, 1);
					StringBuilder sb = new StringBuilder();
					if (addresses.size() > 0) {
						Address address = addresses.get(0);
						for (int i = 0; i < address.getMaxAddressLineIndex(); i++)
							sb.append(address.getAddressLine(i)).append("\n");
						sb.append(address.getCountryName()).append(" ");	// 나라코드
						sb.append(address.getLocality()).append(" ");		// 시
						sb.append(address.getSubLocality() + " ");  		// 구
						sb.append(address.getThoroughfare()).append(" ");	// 동
						sb.append(address.getFeatureName()).append(" ");	// 번지
						addressString = sb.toString();
					}
				} catch (IOException e) {
					e.printStackTrace();
				}
				Log.d(TAG, "당신의 현재 위치는 " + lat + ", " + lon + "이고, " + "주소는 " + addressString + " 입니다");
				locationString = "위도, 경도 : (" + lat + ", " + lon + "), " + "주소 : " + addressString + "";
				addressString = "";
			}
		};

		locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, locationListner);
//		locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListner);
		
		// Wifi
		wifi = (WifiManager) getSystemService(Context.WIFI_SERVICE);
		if (wifi.isWifiEnabled() == false){
			Toast.makeText(mContext, "서명 위치정보 전송을 위해 와이파이가 작동합니다", Toast.LENGTH_SHORT).show();
			wifi.setWifiEnabled(true);
		}
		
		registerReceiver(new BroadcastReceiver() {
			@Override
			public void onReceive(Context context, Intent intent) {
				Log.d(TAG, "Wifi Scan Result Receive");
				scanResultList = wifi.getScanResults();
				scanResultSize = scanResultList.size();
			}
		}, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
		
		wifi.startScan();
	}

	// 변수 연결 및 클릭리스너 설정
	private void setVariable(){
		tvTest = (TextView) findViewById(R.id.tvMainTest);
		btnGcmTest = (Button) findViewById(R.id.btnMainGcmTest);
		btnGcmTest.setOnClickListener(this);

		//		tvProfileID = (TextView) findViewById(R.id.tvMainProfileID);
		tvProfileName = (TextView) findViewById(R.id.tvMainProfileName);
		tvProfileAge = (TextView) findViewById(R.id.tvMainProfileAge);
		tvProfileCourseTerm = (TextView) findViewById(R.id.tvMainProfileCourseTerm);
		tvProfileCourseStep = (TextView) findViewById(R.id.tvMainProfileCourseStep);

		btnNotice = (Button) findViewById(R.id.btnMainNotice);
		btnDocument1 = (Button) findViewById(R.id.btnMainDocument1);
		btnDocument2 = (Button) findViewById(R.id.btnMainDocument2);
		iBtnLogout = (ImageButton) findViewById(R.id.btnMainLogout);

		btnNotice.setOnClickListener(this);
		btnDocument1.setOnClickListener(this);
		btnDocument2.setOnClickListener(this);
		iBtnLogout.setOnClickListener(this);
	}

	// Profile 설정
	private void setProfile(){
		mDataUser = Pref.getDataUser(mContext);
		//		tvProfileID.setText(mDataUser.getUserName());
		tvProfileName.setText(mDataUser.getName());
		tvProfileAge.setText(Integer.toString(mDataUser.getAge()));
		tvProfileCourseTerm.setText(mDataUser.getCourseTerm());
		tvProfileCourseStep.setText(mDataUser.getCourseStep());
	}

	@Override
	public void onClick(View v) {
		Intent intent = null;
		switch(v.getId()){
		case R.id.btnMainGcmTest:
			intent = new Intent(MainActivity.this, GcmTestActivity.class);
			startActivity(intent);
			break;
		case R.id.btnMainNotice:
			new NoticeTask(mContext, "공지사항 목록 로딩중...").execute();
			break;
		case R.id.btnMainDocument1:
			new DocumentListTask(mContext, "문서 목록 로딩중...", "signed").execute();
			break;
		case R.id.btnMainDocument2:
			new DocumentListTask(mContext, "문서 목록 로딩중...", "unsigned").execute();
			break;
		case R.id.btnMainLogout:
			intent = new Intent(MainActivity.this, LoginActivity.class);
			Pref.removeSettingData(mContext);
			startActivity(intent);
			finish();
			break;
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}


	/** GCM **/
	// You need to do the Play Services APK check here too.
	@Override
	protected void onResume() {
		super.onResume();
		checkPlayServices();
	}

	/**
	 * Check the device to make sure it has the Google Play Services APK. If
	 * it doesn't, display a dialog that allows users to download the APK from
	 * the Google Play Store or enable it in the device's system settings.
	 */
	private boolean checkPlayServices() {
		int resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
		if (resultCode != ConnectionResult.SUCCESS) {
			if (GooglePlayServicesUtil.isUserRecoverableError(resultCode)) {
				GooglePlayServicesUtil.getErrorDialog(resultCode, this,
						PLAY_SERVICES_RESOLUTION_REQUEST).show();
			} else {
				Log.i(TAG, "This device is not supported.");
				finish();
			}
			return false;
		}
		return true;
	}

	/**
	 * Gets the current registration ID for application on GCM service.
	 * <p>
	 * If result is empty, the app needs to register.
	 *
	 * @return registration ID, or empty string if there is no existing
	 *         registration ID.
	 */
	private String getRegistrationId(Context context) {
		final SharedPreferences prefs = getGCMPreferences(context);
		String registrationId = prefs.getString(PROPERTY_REG_ID, "");
		if (registrationId.isEmpty()) {
			Log.i(TAG, "Registration not found.");
			return "";
		}
		// Check if app was updated; if so, it must clear the registration ID
		// since the existing regID is not guaranteed to work with the new
		// app version.
		int registeredVersion = prefs.getInt(PROPERTY_APP_VERSION, Integer.MIN_VALUE);
		int currentVersion = getAppVersion(context);
		if (registeredVersion != currentVersion) {
			Log.i(TAG, "App version changed.");
			return "";
		}
		return registrationId;
	}

	/**
	 * @return Application's {@code SharedPreferences}.
	 */
	private SharedPreferences getGCMPreferences(Context context) {
		// This sample app persists the registration ID in shared preferences, but
		// how you store the regID in your app is up to you.
		return getSharedPreferences(MainActivity.class.getSimpleName(),
				Context.MODE_PRIVATE);
	}

	/**
	 * @return Application's version code from the {@code PackageManager}.
	 */
	private static int getAppVersion(Context context) {
		try {
			PackageInfo packageInfo = context.getPackageManager()
					.getPackageInfo(context.getPackageName(), 0);
			return packageInfo.versionCode;
		} catch (NameNotFoundException e) {
			// should never happen
			throw new RuntimeException("Could not get package name: " + e);
		}
	}


	/**
	 * Registers the application with GCM servers asynchronously.
	 * <p>
	 * Stores the registration ID and app versionCode in the application's
	 * shared preferences.
	 */
	private void registerInBackground() {
		new AsyncTask() {
			protected String doInBackground(Object... params) {
				String msg = "";
				try {
					if (gcm == null) {
						gcm = GoogleCloudMessaging.getInstance(mContext);
					}
					regid = gcm.register(SENDER_ID);
					msg = "Device registered, registration ID=" + regid;

					// You should send the registration ID to your server over HTTP,
					// so it can use GCM/HTTP or CCS to send messages to your app.
					// The request to your server should be authenticated if your app
					// is using accounts.
					sendRegistrationIdToBackend(regid);

					// For this demo: we don't need to send it because the device
					// will send upstream messages to a server that echo back the
					// message using the 'from' address in the message.

					// Persist the regID - no need to register again.
					storeRegistrationId(mContext, regid);
				} catch (IOException ex) {
					msg = "Error :" + ex.getMessage();
					// If there is an error, don't just keep trying to register.
					// Require the user to click a button again, or perform
					// exponential back-off.
				}
				return msg;
			}

			protected void onPostExecute(String msg) {
				tvTest.append(msg + "\n");
				new RegistrationTask(mContext, "등록", regid).execute();
			}
		}.execute(null, null, null);
		/**
		 * Sends the registration ID to your server over HTTP, so it can use GCM/HTTP
		 * or CCS to send messages to your app. Not needed for this demo since the
		 * device sends upstream messages to a server that echoes back the message
		 * using the 'from' address in the message.
		 */

	}

	private void sendRegistrationIdToBackend(String reg_id){
		HashMap<String, String> map = new HashMap<String, String>();
		map.put("username", Pref.getDataUser(mContext).getUserName());
		map.put("registration_id", reg_id);
		String resultString = BaseAsyncTask.postRequest(C.API_REG_ANDROID, map);
		Log.d(TAG, "sendRegistrationIdToBackend, resultString:" + resultString);
	}
	/**
	 * Stores the registration ID and app versionCode in the application's
	 * {@code SharedPreferences}.
	 *
	 * @param context application's context.
	 * @param regId registration ID
	 */
	private void storeRegistrationId(Context context, String regId) {
		final SharedPreferences prefs = getGCMPreferences(context);
		int appVersion = getAppVersion(context);
		Log.i(TAG, "Saving regId on app version " + appVersion);
		SharedPreferences.Editor editor = prefs.edit();
		editor.putString(PROPERTY_REG_ID, regId);
		editor.putInt(PROPERTY_APP_VERSION, appVersion);
		editor.commit();
	}

	class RegistrationTask extends BaseAsyncTask2 {
		private String reg_id = "";
		private String resultString = "";

		public RegistrationTask(Context context, String title, String reg_id) {
			super(context, title);
			this.reg_id = reg_id;
		}
		@Override
		protected Integer doInBackground(Void... params) {
			HashMap<String, String> map = new HashMap<String, String>();
			map.put("username", Pref.getDataUser(mContext).getUserName());
			map.put("registration_id", reg_id);
			resultString = postRequest(C.API_REG_ANDROID, map);
			return super.doInBackground(params);
		}
		@Override
		protected void onPostExecute(Integer result) {
			Log.d(TAG, resultString);
			super.onPostExecute(result);
		}
	}

}
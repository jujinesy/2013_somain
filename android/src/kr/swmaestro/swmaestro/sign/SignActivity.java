package kr.swmaestro.swmaestro.sign;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.main.MainActivity;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.Bitmap.CompressFormat;
import android.net.Uri;
import android.net.wifi.ScanResult;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class SignActivity extends ActionBarActivity implements OnClickListener{
	private final String TAG = this.getClass().getSimpleName();
	private int TAKE_CAMERA = 201;
	private Context mContext;

	private SignView mSignView;
	private TextView tvTitle;
	private Button btnOk, btnCamera, btnCancel, btnClear;
	private ImageView ivPhoto;

	private String document_type, document_deadline;
	private int document_id;

	private boolean isCaptured = false;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.sign);
		mContext = this;

		Intent intent = getIntent();
		document_type = intent.getStringExtra("document_type");
		document_deadline = intent.getStringExtra("document_deadline");
		document_id = intent.getIntExtra("document_id", -1);

		mSignView = (SignView) findViewById(R.id.signView);
		tvTitle = (TextView) findViewById(R.id.tvSignTitle);
		btnOk = (Button) findViewById(R.id.signBtnOk);
		btnCamera = (Button) findViewById(R.id.signBtnCamera);
		btnCancel = (Button) findViewById(R.id.signBtnCancel);
		btnClear = (Button) findViewById(R.id.signBtnClear);
		ivPhoto = (ImageView) findViewById(R.id.ivSignPhoto);

		btnOk.setOnClickListener(this);
		btnCamera.setOnClickListener(this);
		btnCancel.setOnClickListener(this);
		btnClear.setOnClickListener(this);

		tvTitle.setText(document_type + " / 마감기한 : " + document_deadline);
		isCaptured = false;
	}

	@Override
	public void onClick(View v) {
		Intent intent = null;
		switch(v.getId()){
		case R.id.signBtnOk:
			//			mSignView.saveView();
			intent = getIntent();
			setResult(RESULT_OK, intent);

			// Wifi
			int rssi = -100;
			String bssi = "";
			String ssid = "";
			Log.d(TAG, "ScanSize : " + MainActivity.scanResultSize);
			for(int i=0; i<MainActivity.scanResultList.size(); i++){
				ScanResult ap = MainActivity.scanResultList.get(i);
				rssi = ap.level;
				bssi = ap.BSSID.toUpperCase();
				ssid = ap.SSID.toString();
				if(ssid.equals("SoMa Center")){
					//					Log.d(TAG, "ScanList[" + i + "] : " + ssid + ", " + bssi + ", " + rssi);
					if(ap.level > rssi){
						bssi = ap.BSSID;
						rssi = ap.level;
						ssid = ap.SSID;
					}
				}
			}
			Log.d(TAG, "Near wifi : " + bssi + ", " + rssi);
			String nearWifi = "NearWifi : " + ssid + ", " + bssi + ", " + "강도 : " + rssi; 
			new SignTask(mContext, "서명정보 전송 중...", mSignView, document_id, nearWifi).execute();
			break;
		case R.id.signBtnCamera:
			Log.d(TAG, "Click Btn Camera");
			intent = new Intent();
			intent.setAction(MediaStore.ACTION_IMAGE_CAPTURE);
			startActivityForResult(intent, TAKE_CAMERA);
			break;
		case R.id.signBtnCancel:
			intent = getIntent();
			setResult(RESULT_OK, intent);
			finish();
			break;
		case R.id.signBtnClear:
			mSignView.clear();
			break;
		}
	}

	@Override
	public void onBackPressed() {
		Intent intent = getIntent();
		setResult(RESULT_OK, intent);
		finish();
	}

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		if(resultCode == RESULT_OK){
			if(requestCode == TAKE_CAMERA){
				Bitmap bm = (Bitmap) data.getExtras().get("data");
				//				Drawable drawable = new BitmapDrawable(bm);
				//				btnCamera.setBackground(drawable);
				ivPhoto.setImageBitmap(bm);

				try {
					String path = Environment.getExternalStorageDirectory().getAbsolutePath();
					File f = new File(path+"/somain");
					f.mkdir();
					File f2 = new File(path + "/somain/photo.jpg");
					FileOutputStream fos = new FileOutputStream(f2);

					if (fos != null){ 
						bm.compress(Bitmap.CompressFormat.PNG, 100, fos); 
						fos.close(); 
					}
					Log.d(TAG, "SignActivity Camera Result Image Save(\"somain/photo.jpg\"");
					isCaptured = true;
				} catch (Exception e)	{
					e.printStackTrace();
				} 
			}
		}
	}

	public String getRealPathFromURI(Uri contentUri){
		String [] proj={MediaStore.Images.Media.DATA};
		Cursor cursor = managedQuery(contentUri, proj, null, null, null); 
		int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
		cursor.moveToFirst();
		return cursor.getString(column_index);

	}









}

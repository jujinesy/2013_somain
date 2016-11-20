package kr.swmaestro.swmaestro.sign;

import java.io.File;
import java.util.HashMap;

import kr.swmaestro.swmaestro.main.MainActivity;
import kr.swmaestro.swmaestro.other.BaseAsyncTask;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;

import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.os.Environment;
import android.util.Log;
import android.widget.Toast;

public class SignTask extends BaseAsyncTask {
	private Context mContext;
	private Activity mActivity;
	private SignView mSignView;
	private int RESULT_OK = 1;
	private int RESULT_FAILED = 0;
	private String resultString;
	private int document_id;
	private String wifi;
	
	private String requestFileName = "sign_image";
	private String fileName, filePath;

	public SignTask(Context context, String title, SignView signView, int document_id, String wifi) {
		super(context, title);
		mContext = context;
		mActivity = (Activity) mContext;
		mSignView = signView;
		this.document_id = document_id;
		this.wifi = wifi;
	}

	@Override
	protected Integer doInBackground(Void... params) {
		// Value Pair
		HashMap<String, String> valuePair = new HashMap<String, String>();
		valuePair.put("session_key", Pref.getDataLogin(mContext).getSessionKey());
		valuePair.put("username", Pref.getDataUser(mContext).getUserName());
		valuePair.put("document_id", Integer.toString(document_id));
		valuePair.put("wifi", this.wifi);
		valuePair.put("location", MainActivity.locationString);
		
		// Sign File
		String signFileName = "/somain/" + "sign_" + Pref.getDataUser(mContext).getUserName() + "_" + Integer.toString(document_id) + ".png";
		boolean isSaveSuccess = mSignView.saveView(signFileName);
		if (! isSaveSuccess){
			return RESULT_FAILED;
		}
		String path = Environment.getExternalStorageDirectory().getAbsolutePath();
		String signFilePath = path + signFileName;

		// Photo File
		String photoFilePath = path + "/somain/" + "photo.jpg";
		
		// File Pair
		HashMap<String, String> filePair = new HashMap<String, String>();
		filePair.put("sign_image", signFilePath);
		filePair.put("photo", photoFilePath);

		resultString = postRequestFile(C.API_SEND_SIGN, valuePair, filePair);
		Log.d(TAG, resultString);
		return RESULT_OK;
	}

	@Override
	protected void onPostExecute(Integer result) {
		if(result==RESULT_OK){
			try{
				JSONObject jsonObject = new JSONObject(resultString);
				String return_status = jsonObject.getString("return_status");
				if(return_status.equals("success")){
					Toast.makeText(mContext, "서명 전송이 완료되었습니다", Toast.LENGTH_SHORT).show();
					mActivity.finish();
				} else if(return_status.equals("failed")){
					Toast.makeText(mContext, "서명 전송에 실패하였습니다", Toast.LENGTH_SHORT).show();
				}
			} catch(Exception e){
				e.printStackTrace();
				Toast.makeText(mContext, "서명 전송에 실패하였습니다", Toast.LENGTH_SHORT).show();
			}
		} else{
			Toast.makeText(mContext, "서명 저장에 실패했습니다", Toast.LENGTH_SHORT).show();
		}
		super.onPostExecute(result);
	}	
}

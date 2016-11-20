package kr.swmaestro.swmaestro.login;

import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;

import kr.swmaestro.swmaestro.main.MainActivity;
import kr.swmaestro.swmaestro.other.BaseAsyncTask;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class LoginTask extends BaseAsyncTask{
	private Context mContext;
	private Activity mActivity;
	private String id, pw;
	private boolean isAutoLogin;
	private String resultString;

	public LoginTask(Context context, String title, String id, String pw, boolean isAutoLogin) {
		super(context, title);
		mContext = context;
		mActivity = (Activity) mContext;
		this.id = id;
		this.pw = pw;
		this.isAutoLogin = isAutoLogin;
	}

	@Override
	protected Integer doInBackground(Void... params) {
		HashMap<String, String> map = new HashMap<String, String>();
		map.put("username", id);
		map.put("password", pw);
		resultString = postRequest(C.API_LOGIN, map);
		return super.doInBackground(params);
	}

	@Override
	protected void onPostExecute(Integer result) {
		super.onPostExecute(result);
		String testString = "";
		try {
			JSONObject jsonObjectResult = new JSONObject(resultString);
			testString = jsonObjectResult.getString("session_key");
			Pref.setLoginStringData(mContext, resultString);

			Pref.setAutoLogin(mContext, isAutoLogin);
			if(isAutoLogin){
				Pref.setIdPw(mContext, id, pw);
			}
			
			Intent intent = new Intent(mActivity, MainActivity.class);
			mActivity.startActivity(intent);
			mActivity.finish();
		} catch (JSONException e) {
			e.printStackTrace();
			Toast.makeText(mContext, "로그인에 실패하였습니다", Toast.LENGTH_SHORT).show();
		}
		
	}	
}

package kr.swmaestro.swmaestro.document;

import java.util.HashMap;

import kr.swmaestro.swmaestro.other.BaseAsyncTask;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;

import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class DocumentListBaseTask extends BaseAsyncTask {
	public Context mContext;
	public Activity mActivity;
	public String type;
	public String resultString;

	public DocumentListBaseTask(Context context, String title, String type) {
		super(context, title);
		mContext = context;
		mActivity = (Activity) mContext;
		this.type = type;
	}

	@Override
	protected Integer doInBackground(Void... params) {
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		HashMap<String, String> map = new HashMap<String, String>();
		map.put("session_key", Pref.getDataLogin(mContext).getSessionKey());
		map.put("type", type);
		map.put("username", Pref.getDataUser(mContext).getUserName());
		
		resultString = postRequest(C.API_DOCUMENT_LIST, map);
		return super.doInBackground(params);
	}

	@Override
	protected void onPostExecute(Integer result) {
		super.onPostExecute(result);
		
		
	}	
}

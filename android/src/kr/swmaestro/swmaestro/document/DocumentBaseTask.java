package kr.swmaestro.swmaestro.document;

import java.util.HashMap;

import kr.swmaestro.swmaestro.other.BaseAsyncTask;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;
import android.content.Context;

public class DocumentBaseTask extends BaseAsyncTask {
	private Context mContext;
	private String document_id;
	private String resultString;

	public DocumentBaseTask(Context context, String title, String document_id) {
		super(context, title);
		mContext = context;
		this.document_id = document_id;
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
		map.put("username", Pref.getDataUser(mContext).getUserName());
		map.put("document_id", document_id);
		
		resultString = postRequest(C.API_DOCUMENT, map);
		return super.doInBackground(params);
	}

	@Override
	protected void onPostExecute(Integer result) {
		
		super.onPostExecute(result);
	}
	
	

}

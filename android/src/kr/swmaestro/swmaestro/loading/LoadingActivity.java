package kr.swmaestro.swmaestro.loading;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.login.LoginActivity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.view.Window;
import android.widget.LinearLayout;
import android.widget.ProgressBar;

public class LoadingActivity extends ActionBarActivity{
	private final String TAG = this.getClass().getSimpleName();
	private Context mContext;
	private LinearLayout llLoadingProgress;
	private ProgressBar mProgressBar;

	private int version_current, version_market;
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		super.onCreate(savedInstanceState);
		setContentView(R.layout.loading);
		mContext = this;
		
		llLoadingProgress = (LinearLayout) findViewById(R.id.llLoadingProgress);
		new VersionCheckTask().execute();
	}
	

	private class VersionCheckTask extends AsyncTask<Void, Void, Void>{
		@Override
		protected void onPreExecute() {
			super.onPreExecute();
			mProgressBar = new ProgressBar(mContext);
			llLoadingProgress.setGravity(Gravity.CENTER_HORIZONTAL);
			llLoadingProgress.addView(mProgressBar, new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
		}

		@Override
		protected Void doInBackground(Void... params) {
			return null;
		}

		@Override
		protected void onPostExecute(Void result) {
			super.onPostExecute(result);
			mProgressBar.setVisibility(View.GONE);
			if(version_current < version_market){
				// show update dialog
			} else{
//				new InitializeTask().execute();
			}
			new InitializeTask().execute();
		}
	}

	private class InitializeTask extends AsyncTask<Void, Void, Void>{
		@Override
		protected void onPreExecute() {
			super.onPreExecute();
			mProgressBar = new ProgressBar(mContext);
			llLoadingProgress.setGravity(Gravity.CENTER_HORIZONTAL);
			llLoadingProgress.addView(mProgressBar, new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
		}

		@Override
		protected Void doInBackground(Void... params) {
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			return null;
		}

		@Override
		protected void onPostExecute(Void result) {
			super.onPostExecute(result);
			mProgressBar.setVisibility(View.GONE);
			Intent intent = new Intent(LoadingActivity.this, LoginActivity.class);
			startActivity(intent);
			finish();
		}
	}
}

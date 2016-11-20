package kr.swmaestro.swmaestro;
import java.io.IOException;
import java.util.concurrent.atomic.AtomicInteger;

import kr.swmaestro.swmaestro.R;
import android.content.Context;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

import com.google.android.gms.gcm.GoogleCloudMessaging;


public class GcmTestActivity extends ActionBarActivity implements OnClickListener{
	private Context mContext;
	private Button btnTest, btnClear;
	private TextView tvTest;
	
	GoogleCloudMessaging gcm;
	String SENDER_ID = "6181800579";
	AtomicInteger msgId = new AtomicInteger();

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.gcmtest);
		
		btnTest = (Button) findViewById(R.id.btnGcmTestSend);
		btnClear = (Button) findViewById(R.id.btnGcmTestClear);
		tvTest = (TextView) findViewById(R.id.tvGcmTest);
		
		btnTest.setOnClickListener(this);
		
		gcm = GoogleCloudMessaging.getInstance(this);
//		regid = getRegistrationId(mContext);
	}

	@Override
	public void onClick(View view) {
		if (view == findViewById(R.id.btnGcmTestSend)) {
	        new AsyncTask() {
	            @Override
	            protected String doInBackground(Object... params) {
	                String msg = "";
	                try {
	                    Bundle data = new Bundle();
	                        data.putString("my_message", "Hello World");
	                        data.putString("my_action",
	                                "com.google.android.gcm.demo.app.ECHO_NOW");
	                        String id = Integer.toString(msgId.incrementAndGet());
	                        gcm.send(SENDER_ID + "@gcm.googleapis.com", id, data);
	                        msg = "Sent message";
	                } catch (IOException ex) {
	                    msg = "Error :" + ex.getMessage();
	                }
	                return msg;
	            }

	            @Override
				protected void onPostExecute(Object result) {
	            		String msg = (String) result;
					tvTest.append(msg + "\n");
				}
	        }.execute(null, null, null);
	    } else if (view == findViewById(R.id.btnGcmTestClear)) {
	        tvTest.setText("");
	    }
		
	}

}

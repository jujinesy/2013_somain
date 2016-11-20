package kr.swmaestro.swmaestro.login;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.other.Pref;
import android.app.NotificationManager;
import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class LoginActivity extends ActionBarActivity implements OnClickListener{
	private final String TAG = this.getClass().getSimpleName();
	private Context mContext;

	private EditText etId, etPw;
	private CheckBox cbAutoLogin;
	private Button btnLogin;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.login2);

		mContext = this;

		etId = (EditText) findViewById(R.id.etLoginId);
		etPw = (EditText) findViewById(R.id.etLoginPw);
		cbAutoLogin = (CheckBox) findViewById(R.id.cbLoginAuto);
		btnLogin = (Button) findViewById(R.id.btnLoginLogin);

		btnLogin.setOnClickListener(this);

		// Test
		//		etId.setText("leehanyeong");
		//		etPw.setText("root");

		if(Pref.getAutoLogin(mContext) == true){
			cbAutoLogin.setChecked(true);
			etId.setText(Pref.getId(mContext));
			etPw.setText(Pref.getPw(mContext));

			String id = etId.getText().toString();
			String pw = etPw.getText().toString();
			new LoginTask(mContext, "로그인 중...", id, pw, cbAutoLogin.isChecked()).execute();
		}

		NotificationManager noti = (NotificationManager)getSystemService(NOTIFICATION_SERVICE); 
		if(noti != null){
			noti.cancel(1);
		}
	}

	@Override
	public void onClick(View v) {
		switch(v.getId()){
		case R.id.btnLoginLogin:
			String id = etId.getText().toString();
			String pw = etPw.getText().toString();
			new LoginTask(mContext, "로그인 중...", id, pw, cbAutoLogin.isChecked()).execute();
		}
	}
}

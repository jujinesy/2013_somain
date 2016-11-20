package kr.swmaestro.swmaestro;
import java.util.ArrayList;

import org.json.JSONException;
import org.json.JSONObject;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataDocument;
import kr.swmaestro.swmaestro.data.DataUser;
import kr.swmaestro.swmaestro.login.LoginActivity;
import android.app.IntentService;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v4.app.NotificationCompat;
import android.util.Log;

import com.google.android.gms.gcm.GoogleCloudMessaging;

public class GcmIntentService extends IntentService {
	private String TAG = this.getClass().getSimpleName();
	public static final int NOTIFICATION_ID = 1;
	private NotificationManager mNotificationManager;
	NotificationCompat.Builder builder;

	public GcmIntentService() {
		super("GcmIntentService");
	}

	@Override
	protected void onHandleIntent(Intent intent) {
		String baseTitle = "SW Maestro Intranet";
		Bundle extras = intent.getExtras();
		GoogleCloudMessaging gcm = GoogleCloudMessaging.getInstance(this);
		// The getMessageType() intent parameter must be the intent you received
		// in your BroadcastReceiver.
		String messageType = gcm.getMessageType(intent);

		if (!extras.isEmpty()) {  // has effect of unparcelling Bundle
			/*
			 * Filter messages based on message type. Since it is likely that GCM
			 * will be extended in the future with new message types, just ignore
			 * any message types you're not interested in, or that you don't
			 * recognize.
			 */
			if (GoogleCloudMessaging.
					MESSAGE_TYPE_SEND_ERROR.equals(messageType)) {
				sendNotification(baseTitle, "Send error: " + extras.toString());
			} else if (GoogleCloudMessaging.
					MESSAGE_TYPE_DELETED.equals(messageType)) {
				sendNotification(baseTitle, "Deleted messages on server: " +
						extras.toString());
				// If it's a regular GCM message, do some work.
			} else if (GoogleCloudMessaging.
					MESSAGE_TYPE_MESSAGE.equals(messageType)) {
				// This loop represents the service doing some work.
				for (int i=0; i<1; i++) {
					Log.i(TAG, "Working... " + (i+1)
							+ "/5 @ " + SystemClock.elapsedRealtime());
					try {
						Thread.sleep(5000);
					} catch (InterruptedException e) {
					}
				}
				Log.i(TAG, "Completed work @ " + SystemClock.elapsedRealtime());
				Log.i(TAG, "Received: " + extras.toString());

				if(((String) extras.getString("type")).equals("normal")){
					String doc_type = "";
					String name = "";
					String created = "";
					String deadline = "";

					try {
						JSONObject dataDocumentJsonObject = new JSONObject((String) extras.get("document"));
						DataDocument dataDocument = new DataDocument(dataDocumentJsonObject);
						doc_type = dataDocument.getDocumentType();
						created = dataDocument.getCreated();
						deadline = dataDocument.getDeadLine();
					} catch (JSONException e) {
						e.printStackTrace();
					}
					sendNotification("SW Maestro Intranet", deadline + "까지 제출해야 하는\n" + doc_type + " 문서가 있습니다");
				} else{
					String title = ((String) extras.getString("title"));
					sendNotification("SW Maestro Intranet", title);
				}

			}
		}
		// Release the wake lock provided by the WakefulBroadcastReceiver.
		GcmBroadcastReceiver.completeWakefulIntent(intent);
	}

	// Put the message into a notification and post it.
	// This is just one simple example of what you might choose to do with
	// a GCM message.
	private void sendNotification(String title, String msg) {
		mNotificationManager = (NotificationManager)
				this.getSystemService(Context.NOTIFICATION_SERVICE);

		PendingIntent contentIntent = PendingIntent.getActivity(this, 0,
				new Intent(this, LoginActivity.class), 0);

		NotificationCompat.Builder mBuilder =
				new NotificationCompat.Builder(this)
		.setSmallIcon(R.drawable.push_btn)
		.setContentTitle(title)
		.setStyle(new NotificationCompat.BigTextStyle()
		.bigText(msg))
		.setContentText(msg);

		mBuilder.setContentIntent(contentIntent);
		Notification noti = mBuilder.build();
		noti.flags |= Notification.FLAG_AUTO_CANCEL;
		mNotificationManager.notify(NOTIFICATION_ID, noti);
	}
}
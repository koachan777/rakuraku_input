from django.urls import path, include

from rakuraku_apps.views.common import (
    CustomLoginView,
    HomeView, 
    CustomLoginView,
    LogoutView, 
    SignupView
)
from rakuraku_apps.views.everyday_input import (
    EverydayCommentInputView, 
    EverydayConfirmInputView, 
    EverydayEditView, 
    EverydayFirstInputView, 
    EverydayOrIntervalView, 
    EverydaySecondInputView
)
from rakuraku_apps.views.interval_input import (
    IntervalCommentInputView, 
    IntervalConfirmInputView, 
    IntervalEditView, 
    IntervalFirstInputView, 
    IntervalSecondInputView, 
    IntervalThirdInputView
)
from rakuraku_apps.views.log import (
    GraphView, 
    TableOrGraphView, 
    TableView
)
from rakuraku_apps.views.manage import (
    CreateShrimpView,
    CreateTankView,
    ManageValueView, 
    ManageTankView, 
    ManageUserView, 
    ManageView
)

app_name = "rakuraku_apps"

urlpatterns = [
    # ログイン画面
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),

    # ユーザー新規登録画面
    path('signup/', SignupView.as_view(), name='signup'),

    # ホーム画面　機能選択
    path('home/', HomeView.as_view(), name='home'),

    # データ入力　日常測定・定期測定選択画面
    path('everyday_or_interval/', EverydayOrIntervalView.as_view(), name='everyday_or_interval'),

    # データ入力　日常入力１　日付・水槽・室温
    path('everyday/first_input/', EverydayFirstInputView.as_view(), name='everyday_first_input'),

    # データ入力　日常入力２　水温・pH・DO・塩分濃度
    path('everyday/second_input/', EverydaySecondInputView.as_view(), name='everyday_second_input'),

    # データ入力　日常入力３　備考
    path('everyday/comment/', EverydayCommentInputView.as_view(), name='everyday_comment'),

    # データ入力　日常入力４　確認画面
    path('everyday/confirm/', EverydayConfirmInputView.as_view(), name='everyday_confirm'),

    # データ入力　日常入力５　編集画面
    path('everyday/edit/', EverydayEditView.as_view(), name='everyday_edit'),

    # データ入力　定期測定１　日付・水槽・室温
    path('interval/first_input/', IntervalFirstInputView.as_view(), name='interval_first_input'),

    # データ入力　定期測定２　NH4・NO2・NO3
    path('interval/second_input/', IntervalSecondInputView.as_view(), name='interval_second_input'),

    # データ入力　定期測定３　Ca・Al・Mg
    path('interval/third_input/', IntervalThirdInputView.as_view(), name='interval_third_input'),

    # データ入力　定期測定４　備考
    path('interval/comment/', IntervalCommentInputView.as_view(), name='interval_comment'),

    # データ入力　定期測定５　確認画面
    path('interval/confirm/', IntervalConfirmInputView.as_view(), name='interval_confirm'),

    # データ入力　定期測定６　編集画面
    path('interval/edit/', IntervalEditView.as_view(), name='interval_edit'),

    # 過去のデータ　表・グラフ選択画面
    path('table_or_graph/', TableOrGraphView.as_view(), name='table_or_graph'),

    # 過去のデータ　表
    path('table/', TableView.as_view(), name='table'),

    # 過去のデータ　グラフ
    path('graph/', GraphView.as_view(), name='graph'),

    # 管理者画面　ホーム（ユーザー・水槽・水質基準値・警告範囲）
    path('manage/', ManageView.as_view(), name='manage'),

    # 管理者画面　ユーザー
    path('manage/user/', ManageUserView.as_view(), name='manage_user'),

    # 管理者画面　水槽
    path('manage/tank/', ManageTankView.as_view(), name='manage_tank'),

    path('manage/create_tank', CreateTankView.as_view(), name='create_tank'),
    path('manage/create_shrimp', CreateShrimpView.as_view(), name='create_shrimp'),

    # 管理者画面　水質基準値
    path('manage/value/', ManageValueView.as_view(), name='manage_value'),

]
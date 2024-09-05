from django.urls import path, include
from .views import log

from rakuraku_apps.views.common import (
    CustomLoginView,
    FunctionView,
    HomeView, 
    CustomLoginView,
    LogoutView,
    Omake10View,
    Omake1View,
    Omake2View,
    Omake3View,
    Omake4View,
    Omake5View,
    Omake6View,
    Omake7View,
    Omake8View,
    Omake9View,
    OmakeView, 
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
    TableView,
    export_to_excel
)
from rakuraku_apps.views.manage import (
    CreateShrimpView,
    CreateTankView,
    DeleteTankView,
    DeleteUserView,
    ManageValueView, 
    ManageTankView, 
    ManageUserView, 
    ManageView
)

app_name = "rakuraku_apps"

urlpatterns = [
    # ログイン画面
    path('', CustomLoginView.as_view(), name='login'),

    # ログアウト
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

    # 過去のデータ　表　編集画面
    path('edit_water_quality/<int:pk>/', log.edit_water_quality, name='edit_water_quality'),

    # 過去のデータ　表　削除
    path('delete_water_quality/<int:pk>/', log.delete_water_quality, name='delete_water_quality'),

    # 過去のデータ　表　excel
    path('export_to_excel/', export_to_excel, name='export_to_excel'),

    # 過去のデータ　グラフ
    path('graph/', GraphView.as_view(), name='graph'),

    # 管理者画面　ホーム（ユーザー・水槽・水質基準値・警告範囲）
    path('manage/', ManageView.as_view(), name='manage'),

    # 管理者画面　ユーザー
    path('manage/user/', ManageUserView.as_view(), name='manage_user'),

    # 管理者画面　ユーザー削除
    path('manage/user/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

    # 管理者画面　水槽
    path('manage/tank/', ManageTankView.as_view(), name='manage_tank'),

    # 管理者画面　水槽削除
    path('manage/tank/<int:pk>/delete/', DeleteTankView.as_view(), name='delete_tank'),

    # 管理者画面　水槽作成
    path('manage/create_tank', CreateTankView.as_view(), name='create_tank'),

    # 管理者画面　系統作成
    path('manage/create_shrimp', CreateShrimpView.as_view(), name='create_shrimp'),

    # 管理者画面　水質基準値
    path('manage/value/', ManageValueView.as_view(), name='manage_value'),

    # 機能紹介
    path('function', FunctionView.as_view(), name='function'),

    # おまけ
    path('omake', OmakeView.as_view(), name='omake'),

    # おまけ1
    path('omake1', Omake1View.as_view(), name='omake1'),

    # おまけ2
    path('omake2', Omake2View.as_view(), name='omake2'),

    # おまけ3
    path('omake3', Omake3View.as_view(), name='omake3'),

    # おまけ4
    path('omake4', Omake4View.as_view(), name='omake4'),

    # おまけ5
    path('omake5', Omake5View.as_view(), name='omake5'),

    # おまけ6
    path('omake6', Omake6View.as_view(), name='omake6'),

    # おまけ7
    path('omake7', Omake7View.as_view(), name='omake7'),

    # おまけ8
    path('omake8', Omake8View.as_view(), name='omake8'),

    # おまけ9
    path('omake9', Omake9View.as_view(), name='omake9'),

    # おまけ10
    path('omake10', Omake10View.as_view(), name='omake10'),
]
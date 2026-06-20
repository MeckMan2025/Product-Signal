from product_signal import reddit_client


def test_user_agent_format():
    ua = reddit_client.build_user_agent("Lanky_Flounder2906", version="2.0.0")
    assert ua == "macos:com.productsignal.research:v2.0.0 (by /u/Lanky_Flounder2906)"


def test_user_agent_includes_username():
    ua = reddit_client.build_user_agent("someuser")
    assert "/u/someuser" in ua
    assert ua.startswith("macos:com.productsignal.research:")

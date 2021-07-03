function main(splash)
    assert(splash:go(splash.args.url))
    assert(splash:wait(5))

    -- find and click button corresponding to `selector`
    -- this may be a link or a JS button
    btn = assert(
        splash:select(
            splash.args.selector
        ),
        'CSS selector did not match any buttons'
    )
    btn:mouse_click()

    assert(splash:wait(5))
    return {
        url = splash:url(),
        html = splash:html()
    }
end
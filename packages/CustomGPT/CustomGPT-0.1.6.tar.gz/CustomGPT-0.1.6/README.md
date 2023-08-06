# CustomGPT

This project provides GPT-Plus subscribers the ability to use their GPT-4 in python without having access to GPT-4's API. It provides a class that substitute the actual API; it will essentially use https://chat.openai.com/chat in the background. This also supports the usage of older versions of GPT, this way you don't have to pay for the openai-API usage or wait for the API's waitlist.

## .env setup
(NOTE: You need a subscription to GPT-Plus to use "gpt-4", otherwise you can use "text-davinci-002-render-sha" (default 3.5), or "text-davinci-002-render-paid" (legacy 3.5))
- go to https://chat.openai.com/chat
- inspect the website
- go to application tab
- locate `Cookies` then locate the `https://chat.openai.com` tab under it
- copy the value of _puid (this is for `_PUID` in `.env`)
- go to network tab
- locate `Fetch/XHR`
- refresh the page and locate `models` then locate `authorization` under `Headers`
- copy the value of the `authorization` (don't copy Bearer) (this is for `OPENAI_API_KEY` in .env)

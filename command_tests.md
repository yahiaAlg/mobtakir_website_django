```bash
curl -X POST http://0.0.0.0:11434/api/generate -d '{"prompt": "hi there", "model": "phi3", "system": "you are a casual person", "format": ""}'
```

```json
{
  "prompt": "hi there",
  "model": "phi3",
  "system": "you are a casual person",
  "format": ""
}
```

as a professional website front end developer, create me a full fledged landing-page using BS5 and font Awesome and free Images API service about Translation with sticky navbar and hero, services, how it works, pricings, testimonials, footer containing sitemap, sections using gorgeous style and your ingeniousity

<div id="chat-form" class="w-100 d-flex flex-row justify-content-center align-items-between">
    <input type="hidden" name="csrfmiddlewaretoken" value="Dtf9pEvMqjx4adxJwSZDWd8KdTGaMbQC6Nyejj1rxQqzs6cczs6Wvtf0kfWx9Gdn">
    <div class="text-input-area w-75 me-1">
        <div class="input-buttons">
            <button class="input-button" title="Upload Image">
            <i class="fas fa-image"></i>
            </button>
            <button class="input-button" title="Upload File">
            <i class="fas fa-paperclip"></i>
            </button>
            <button class="input-button" title="Record Audio">
            <i class="fas fa-microphone"></i>
            </button>
            <button class="input-button" title="Code Snippet">
            <i class="fas fa-code"></i>
            </button>
        </div>
        <textarea id="user-input" class="text-input" placeholder="Type your message..." rows="1" style="height: 247px;"></textarea>
    </div>
    <button type="submit" class="send-button w-25" id="send-button">
        <i class="fas fa-paper-plane"></i>
    </button>
</div>

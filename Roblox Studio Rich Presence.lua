local HttpService = game:GetService("HttpService")
local StudioService = game:GetService("StudioService")
local MarketPlaceService = game:GetService("MarketplaceService")

local toolbar = plugin:CreateToolbar("Studio Discord Presence")
local toggleButton = toolbar:CreateButton("Studio Discord Presence", "Studio Discord Presence", "rbxassetid://11250270577")
local enabled = false
local gameName = nil

local function makeRequest(data)
	pcall(function()
		HttpService:RequestAsync({
			Url = "http://127.0.0.1:24981",
			Method = "POST",
			Headers = {
				["Content-Type"] = "application/json"
			},
			Body = HttpService:JSONEncode(data)
		})
	end)
end

local function updatePresence()
	if enabled then
		local activeScript = StudioService.ActiveScript or workspace
		local scriptType = activeScript.ClassName
		
		if not gameName then
			gameName = MarketPlaceService:GetProductInfo(game.PlaceId).Name
		end
		
		local data = {
			scriptName = activeScript.Name,
			scriptType = activeScript.ClassName,
			gameName = game.Name
		}
		
		makeRequest(data)
	end
end

toggleButton.Click:Connect(function()
	enabled = not enabled
	updatePresence()
end)

StudioService:GetPropertyChangedSignal("ActiveScript"):Connect(updatePresence)
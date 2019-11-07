import csv

class SlackAnalytics:

	def __init__(self):
		self.totalEmojiUsage = {}
		self.emojiPostUsage = {}
		self.emojiReactionUsage = {}

	def incrementEmojiPostUsage(self, emojiName, amount):
		self.increment(emojiName, self.emojiPostUsage, amount)
		self.increment(emojiName, self.totalEmojiUsage, amount)

	def incrementEmojiReactionUsage(self, emojiName, amount):
		self.increment(emojiName, self.emojiReactionUsage, amount)
		self.increment(emojiName, self.totalEmojiUsage, amount)

	def increment(self, emojiName, dict, amount):
		if emojiName not in dict:
			dict[emojiName] = 0
		dict[emojiName] = dict[emojiName] + amount

	def report(self):
		self.writeDictToCsv('emoji_usage_total', self.totalEmojiUsage)
		self.writeDictToCsv('emoji_usage_post', self.emojiPostUsage)
		self.writeDictToCsv('emoji_usage_reaction', self.emojiReactionUsage)

	def writeDictToCsv(self, fileName, dict):
		with open(f'{fileName}.csv', mode='w') as file:
			writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

			writer.writerow(['emojiName', 'count'])
			for emojiName in dict:
				writer.writerow([emojiName, dict[emojiName]])

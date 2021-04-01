from discord.ext import commands, tasks
import discord 
import os
import time

client = commands.Bot(command_prefix = "t!", help_command=None)

Token = "my_token"

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="My Ungrateful Life"))
    print("We have logged in as {}".format(client.user))

@client.command()
async def help(ctx):
    context = """```List of Commands!
    1. t!ping                         
    = return ping
    2. t!all                          
    = return all of registered tasks
    3. t!add <nama> <tanggal> <waktu> 
    = If you want to input a task
    4. t!update <target tugas> <choice> <new data>
    = If you want to update a value, before that you must specifiy which tugas you want to edit, 
    which value do you want to change, and the new data that you want to insert
    5. t!delete <nama>                
    = If you want to delete a task based from it's name
    6. t!clear <number> (default value = 100)               
    = If you want to delete messages regardless if you have the permission or not 
        (Use it wisely!!!)
    (Example: t!clear 3, it gonna clear 3 messages above this command)
    7. t!help                         
    = Show this messages```"""
    await ctx.send(context)

@client.command()
async def ping(ctx):
    await ctx.send(str(round(client.latency * 100)) + "ms")

@client.command()
async def all(ctx):
    f = open("data.txt","r")
    contents = f.read().split("\n\n")
    if len(contents) == 1 :
        await ctx.send("```Data masih kosong```")
    else:
        count = 1
        for content in contents:
            if len(content) > 1:
                await ctx.send("**" + "Task " + str(count) + "**\n" + "```" + content + "```")
                count += 1

@client.command()
async def add(ctx, nama, tanggal, waktu):
    f = open("data.txt","a+")
    #Tulisannya kenapa gini karena agar ngepas ketika dipush ke discord
    f.write("Nama\t\t\t\t\t\t\t: {}\nTanggal Deadline\t\t\t\t: {}\nWaktu Deadline\t\t\t\t  : {}\r\n\n".format(nama, tanggal, waktu))
    f.close()
    msg = await ctx.send("Data telah dimasukkan")
    time.sleep(5)
    await msg.delete()

@client.command()
async def update(ctx, primary_nama, choice, data_baru):
    f = open("data.txt", "r")
    #Ambil semua datanya
    contents = f.read().split("\n\n")
    for x in range(len(contents)):
        if primary_nama in contents[x]:
            target_data = contents[x].split("\n")
            for y in range(len(target_data)):
                if choice in target_data[y]:
                    target = target_data[y].split(": ")
                    print(target)
                    target[1] = data_baru
                    target_data[y] = ": ".join(target)
                    print(target_data)
                    contents[x] = "\n".join(target_data)
                    print(contents)
                    break
    contents = "\n\n".join(contents)
    with open("data.txt", "w") as f:
        f.write(contents)
        f.close()
    msg = await ctx.send("Data telah diupdate")
    time.sleep(5)
    await msg.delete()

@client.command()
async def delete(ctx, choice):
    f = open("data.txt", "r")
    #Ambil semua datanya
    contents = f.read().split("\n\n")
    #Loop datanya untuk mencari data yang ingin dihapus dan menghilangkannya
    for x in range(len(contents)):
        if choice in contents[x]:
            contents.pop(x)
            for y in range(x, len(contents)):
                #Agar data yang dibawah data yang telah dihapus tetap sesuai formatting awal
                contents[y] = "\n\n" + contents[y]
            break
    f.close()
    status = False
    # #Ngecek apakah datanya yang setelah dihapus tadi itu menjadi kosong atau ternyata ada isinya
    for line in contents:
        for data in line:
            if data.isalnum():
                print("Terdapat Alpha")
                status = True
                break
    # #Jika ternyata ada berarti min. ada 1 data didalam maka praktiknya beda
    if status:
    #     #Terdapat 2 kondisi, yang dihapusnya di tengah atau paling belakang
    #     #Codingan dibawah berhasil jika yang dihapus adalah yang paling bawah
        contents = "".join(contents)
        with open("data.txt", "w") as f:
            f.write(contents)
            f.close
    # #Jika data tidak ada maka txtnya akan di reset menjadi kosong untuk menghilangkan beberapa whitespace
    elif status == False:
        os.remove("data.txt")
        f = open("data.txt", "w")       
        f.close()
        print("Data telah terhapus semua")
    msg = await ctx.send("Data telah dihapus")
    time.sleep(5)
    await msg.delete()

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
        messages.append(message)
    await channel.delete_messages(messages)
    msg = await ctx.send('Messaged deleted.')
    time.sleep(5)
    await msg.delete()

client.run(Token)

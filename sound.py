import winsound

def playsound(sound):
    try:
        winsound.PlaySound("sounds/" + sound+".wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
        return
    except Exception as e:
        print(e)
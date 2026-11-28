def player(prev_play, opponent_history=[], 
           counts={"1": {}, "2": {}, "3": {}}):
    
    # Reset state di awal setiap match baru
    if not prev_play:
        opponent_history.clear()
        for k in counts:
            counts[k].clear()
        return "P"  # Langkah pembuka default
        
    opponent_history.append(prev_play)
    
    # Update frekuensi transisi 1-gram, 2-gram, dan 3-gram
    if len(opponent_history) >= 2:
        last_one = opponent_history[-2]
        next_one = opponent_history[-1]
        if last_one not in counts["1"]:
            counts["1"][last_one] = {}
        counts["1"][last_one][next_one] = counts["1"][last_one].get(next_one, 0) + 1
        
    if len(opponent_history) >= 3:
        last_two = "".join(opponent_history[-3:-1])
        next_one = opponent_history[-1]
        if last_two not in counts["2"]:
            counts["2"][last_two] = {}
        counts["2"][last_two][next_one] = counts["2"][last_two].get(next_one, 0) + 1
        
    if len(opponent_history) >= 4:
        last_three = "".join(opponent_history[-4:-1])
        next_one = opponent_history[-1]
        if last_three not in counts["3"]:
            counts["3"][last_three] = {}
        counts["3"][last_three][next_one] = counts["3"][last_three].get(next_one, 0) + 1

    # Prediksi langkah lawan selanjutnya berdasarkan pola dengan konteks terpanjang yang tersedia
    prediction = None
    
    if len(opponent_history) >= 4:
        last_three = "".join(opponent_history[-3:])
        if last_three in counts["3"]:
            prediction = max(counts["3"][last_three], key=counts["3"][last_three].get)
            
    if prediction is None and len(opponent_history) >= 3:
        last_two = "".join(opponent_history[-2:])
        if last_two in counts["2"]:
            prediction = max(counts["2"][last_two], key=counts["2"][last_two].get)
            
    if prediction is None and len(opponent_history) >= 2:
        last_one = opponent_history[-1]
        if last_one in counts["1"]:
            prediction = max(counts["1"][last_one], key=counts["1"][last_one].get)
            
    # Fallback jika belum ada pola yang terdeteksi
    if prediction is None:
        prediction = "R"
        
    # Counter prediksi lawan
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class DestroyOnClick : MonoBehaviour
{

    public GameObject player;
    public GameObject valid_checker;
    
    void Start() {
        player = GameObject.Find("Player");
        valid_checker = GameObject.Find("Valid_Check");
    }
    
    public static Boolean started = false;
    
    private void OnMouseDown()
    {
        if (started == false) {
            int tag_i = Int32.Parse(gameObject.tag);
            if (tag_i <= 27) {
                List<char> code = BlocksCopy_4.temp_spawn_code;
                code[tag_i-1] = '0';
                BlocksCopy_4 scrpt = player.GetComponent<BlocksCopy_4>();
                scrpt.NewTempCode_r(code);
            } else {
                List<char> code = BlocksCopy.temp_spawn_code;
                code[tag_i-28] = '0';
                BlocksCopy scrpt = player.GetComponent<BlocksCopy>();
                scrpt.NewTempCode_l(code);
            }
            Destroy(gameObject);
            DetectFall checker = valid_checker.GetComponent<DetectFall>();
            checker.FallingState();
        }
    }
}

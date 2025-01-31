using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DetectFall : MonoBehaviour
{
    public bool valid;
    public Renderer matRend;
    public Material valid_mat;
    public Material invalid_mat;
    void Start() {
        matRend = GetComponent<Renderer>(); 
    }
    public void ChangeMat(int state) {
        if (state == 1) {
            matRend.material = valid_mat;
        } else {
            matRend.material = invalid_mat;
        }
    }
    public bool FallingState() {
        for (int a = 0; a < 27; a = a+3) {
            for (int b = 0; b < 2; b++) {
                if (BlocksCopy.temp_spawn_code[a+b] == '0') {
                    if (BlocksCopy.temp_spawn_code[a+b+1] == '0') {
                        ChangeMat(0);
                        return false;
                    }
                }
            }
            if (BlocksCopy.temp_spawn_code[a+0] == '0' && BlocksCopy.temp_spawn_code[a+1] == '0' && BlocksCopy.temp_spawn_code[a+2] == '0') {
                ChangeMat(0);
                return false;
            }
        }
        for (int a = 0; a < 27; a = a+3) {
            for (int b = 0; b < 2; b++) {
                if (BlocksCopy_4.temp_spawn_code[a+b] == '0') {
                    if (BlocksCopy_4.temp_spawn_code[a+b+1] == '0') {
                        ChangeMat(0);
                        return false;
                    }
                }
            }
            if (BlocksCopy_4.temp_spawn_code[a+0] == '0' && BlocksCopy_4.temp_spawn_code[a+1] == '0' && BlocksCopy_4.temp_spawn_code[a+2] == '0') {
                ChangeMat(0);
                return false;
            }
        }
        ChangeMat(1);
        return true;
    }
}

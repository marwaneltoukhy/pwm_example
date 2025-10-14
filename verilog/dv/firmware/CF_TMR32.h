/*
	Copyright 2024-2025 ChipFoundry, a DBA of Umbralogic Technologies LLC.

	Original Copyright 2024 Efabless Corp.
	Author: Efabless Corp. (ip_admin@efabless.com)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

#ifndef CF_TMR32_H
#define CF_TMR32_H

#include "CF_Driver_Common.h"

/* CTRL register bit positions */
#define CF_TMR32_CTRL_REG_TE_BIT	    (uint32_t)(0)
#define CF_TMR32_CTRL_REG_TE_MASK	    (uint32_t)(0x1)
#define CF_TMR32_CTRL_REG_TS_BIT	    (uint32_t)(1)
#define CF_TMR32_CTRL_REG_TS_MASK	    (uint32_t)(0x2)
#define CF_TMR32_CTRL_REG_P0E_BIT	    (uint32_t)(2)
#define CF_TMR32_CTRL_REG_P0E_MASK	    (uint32_t)(0x4)
#define CF_TMR32_CTRL_REG_P1E_BIT	    (uint32_t)(3)
#define CF_TMR32_CTRL_REG_P1E_MASK	    (uint32_t)(0x8)
#define CF_TMR32_CTRL_REG_DTE_BIT	    (uint32_t)(4)
#define CF_TMR32_CTRL_REG_DTE_MASK	    (uint32_t)(0x10)
#define CF_TMR32_CTRL_REG_PI0_BIT	    (uint32_t)(5)
#define CF_TMR32_CTRL_REG_PI0_MASK	    (uint32_t)(0x20)
#define CF_TMR32_CTRL_REG_PI1_BIT	    (uint32_t)(6)
#define CF_TMR32_CTRL_REG_PI1_MASK	    (uint32_t)(0x40)

/* CFG register fields */
#define CF_TMR32_CFG_REG_DIR_BIT	    (uint32_t)(0)
#define CF_TMR32_CFG_REG_DIR_MASK	    (uint32_t)(0x3)
#define CF_TMR32_CFG_REG_P_BIT	        (uint32_t)(2)
#define CF_TMR32_CFG_REG_P_MASK	        (uint32_t)(0x4)

/* PWM configuration fields */
#define CF_TMR32_PWM0CFG_REG_E0_BIT	    (uint32_t)(0)
#define CF_TMR32_PWM0CFG_REG_E0_MASK	(uint32_t)(0x3)
#define CF_TMR32_PWM0CFG_REG_E1_BIT	    (uint32_t)(2)
#define CF_TMR32_PWM0CFG_REG_E1_MASK	(uint32_t)(0xc)
#define CF_TMR32_PWM0CFG_REG_E2_BIT	    (uint32_t)(4)
#define CF_TMR32_PWM0CFG_REG_E2_MASK	(uint32_t)(0x30)
#define CF_TMR32_PWM0CFG_REG_E3_BIT	    (uint32_t)(6)
#define CF_TMR32_PWM0CFG_REG_E3_MASK	(uint32_t)(0xc0)
#define CF_TMR32_PWM0CFG_REG_E4_BIT	    (uint32_t)(8)
#define CF_TMR32_PWM0CFG_REG_E4_MASK	(uint32_t)(0x300)
#define CF_TMR32_PWM0CFG_REG_E5_BIT	    (uint32_t)(10)
#define CF_TMR32_PWM0CFG_REG_E5_MASK	(uint32_t)(0xc00)

#define CF_TMR32_PWM1CFG_REG_E0_BIT	    (uint32_t)(0)
#define CF_TMR32_PWM1CFG_REG_E0_MASK	(uint32_t)(0x3)
#define CF_TMR32_PWM1CFG_REG_E1_BIT	    (uint32_t)(2)
#define CF_TMR32_PWM1CFG_REG_E1_MASK	(uint32_t)(0xc)
#define CF_TMR32_PWM1CFG_REG_E2_BIT	    (uint32_t)(4)
#define CF_TMR32_PWM1CFG_REG_E2_MASK	(uint32_t)(0x30)
#define CF_TMR32_PWM1CFG_REG_E3_BIT	    (uint32_t)(6)
#define CF_TMR32_PWM1CFG_REG_E3_MASK	(uint32_t)(0xc0)
#define CF_TMR32_PWM1CFG_REG_E4_BIT	    (uint32_t)(8)
#define CF_TMR32_PWM1CFG_REG_E4_MASK	(uint32_t)(0x300)
#define CF_TMR32_PWM1CFG_REG_E5_BIT	    (uint32_t)(10)
#define CF_TMR32_PWM1CFG_REG_E5_MASK	(uint32_t)(0xc00)

/* Interrupt flags */
#define CF_TMR32_TO_FLAG	            ((uint32_t)0x1)
#define CF_TMR32_MX_FLAG	            ((uint32_t)0x2)
#define CF_TMR32_MY_FLAG	            ((uint32_t)0x4)

/* PWM actions */
#define CF_TMR32_ACTION_NONE            ((uint32_t)0)
#define CF_TMR32_ACTION_LOW             ((uint32_t)1)
#define CF_TMR32_ACTION_HIGH            ((uint32_t)2)
#define CF_TMR32_ACTION_INVERT          ((uint32_t)3)
#define CF_TMR32_ACTION_MAX_VALUE       ((uint32_t)3)

/* Register limits */
#define CF_TMR32_PWMDT_MAX_VALUE        ((uint32_t)0x000000FF)
#define CF_TMR32_PR_MAX_VALUE           ((uint32_t)0x0000FFFF)
#define CF_TMR32_IM_MAX_VALUE           ((uint32_t)7)
#define CF_TMR32_ICR_MAX_VALUE          ((uint32_t)7)

typedef struct _CF_TMR32_TYPE_ {
	__R 	TMR;
	__W 	RELOAD;
	__W 	PR;
	__W 	CMPX;
	__W 	CMPY;
	__W 	CTRL;
	__W 	CFG;
	__W 	PWM0CFG;
	__W 	PWM1CFG;
	__W 	PWMDT;
	__W 	PWMFC;
	__R 	reserved_0[16309];
	__RW	IM;
	__R 	MIS;
	__R 	RIS;
	__W 	IC;
	__W 	GCLK;
} CF_TMR32_TYPE;

typedef CF_TMR32_TYPE* CF_TMR32_TYPE_PTR;

/* Clock and basic timer control */
CF_DRIVER_STATUS CF_TMR32_setGclkEnable(CF_TMR32_TYPE_PTR tmr32, uint32_t value);
CF_DRIVER_STATUS CF_TMR32_enable(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_disable(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_restart(CF_TMR32_TYPE_PTR tmr32);

/* PWM enable and inversion controls */
CF_DRIVER_STATUS CF_TMR32_PWM0Enable(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_PWM1Enable(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_PWMDeadtimeEnable(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_PWM0Invert(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_PWM1Invert(CF_TMR32_TYPE_PTR tmr32);

/* Timer mode selection */
CF_DRIVER_STATUS CF_TMR32_setUpCount(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_setDownCount(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_setUpDownCount(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_setPeriodic(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_setOneShot(CF_TMR32_TYPE_PTR tmr32);

/* PWM0 action configuration */
CF_DRIVER_STATUS CF_TMR32_setPWM0MatchingZeroAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM0MatchingCMPXUpCountAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM0MatchingCMPYUpCountAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM0MatchingRELOADAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM0MatchingCMPYDownCountAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM0MatchingCMPXDownCountAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);

/* PWM1 action configuration */
CF_DRIVER_STATUS CF_TMR32_setPWM1MatchingZeroAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM1MatchingCMPXUpCountingAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM1MatchingCMPYUpCountingAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM1MatchingRELOADAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM1MatchingCMPYDownCountAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);
CF_DRIVER_STATUS CF_TMR32_setPWM1MatchingCMPXDownCountAction(CF_TMR32_TYPE_PTR tmr32, uint32_t action);

/* Register access helpers */
CF_DRIVER_STATUS CF_TMR32_setRELOAD(CF_TMR32_TYPE_PTR tmr32, uint32_t value);
CF_DRIVER_STATUS CF_TMR32_setCMPX(CF_TMR32_TYPE_PTR tmr32, uint32_t value);
CF_DRIVER_STATUS CF_TMR32_getCMPX(CF_TMR32_TYPE_PTR tmr32, uint32_t *value);
CF_DRIVER_STATUS CF_TMR32_getCMPY(CF_TMR32_TYPE_PTR tmr32, uint32_t *value);
CF_DRIVER_STATUS CF_TMR32_setCMPY(CF_TMR32_TYPE_PTR tmr32, uint32_t value);
CF_DRIVER_STATUS CF_TMR32_getTMR(CF_TMR32_TYPE_PTR tmr32, uint32_t* tmr_value);
CF_DRIVER_STATUS CF_TMR32_setPWMDeadtime(CF_TMR32_TYPE_PTR tmr32, uint32_t value);
CF_DRIVER_STATUS CF_TMR32_setPR(CF_TMR32_TYPE_PTR tmr32, uint32_t value);

/* Interrupt and status helpers */
CF_DRIVER_STATUS CF_TMR32_getRIS(CF_TMR32_TYPE_PTR tmr32, uint32_t* ris_value);
CF_DRIVER_STATUS CF_TMR32_getMIS(CF_TMR32_TYPE_PTR tmr32, uint32_t* mis_value);
CF_DRIVER_STATUS CF_TMR32_setIM(CF_TMR32_TYPE_PTR tmr32, uint32_t mask);
CF_DRIVER_STATUS CF_TMR32_getIM(CF_TMR32_TYPE_PTR tmr32, uint32_t* im_value);
CF_DRIVER_STATUS CF_TMR32_setICR(CF_TMR32_TYPE_PTR tmr32, uint32_t mask);
CF_DRIVER_STATUS CF_TMR32_isTimout(CF_TMR32_TYPE_PTR tmr32, bool* timeout_status);
CF_DRIVER_STATUS CF_TMR32_isCMPXMatch(CF_TMR32_TYPE_PTR tmr32, bool* match_status);
CF_DRIVER_STATUS CF_TMR32_isCMPYMatch(CF_TMR32_TYPE_PTR tmr32, bool* match_status);
CF_DRIVER_STATUS CF_TMR32_clearTimoutFlag(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_clearCMPXMatchFlag(CF_TMR32_TYPE_PTR tmr32);
CF_DRIVER_STATUS CF_TMR32_clearCMPYMatchFlag(CF_TMR32_TYPE_PTR tmr32);


/* Agent test helper */
/**
 * Configure TMR32 for the reference PWM demo used by the firmware tests.
 * This is deliberately simple so agents can reuse the same baseline sequence.
 */
void CF_TMR32_configureExamplePWM(CF_TMR32_TYPE_PTR tmr32);

#endif /* CF_TMR32_H */
